import urllib.request
import glob, re, json
from intake_esgf import ESGFCatalog
import pandas as pd
import xarray as xr
from typing import List, Optional


def source_id_in_activity(activity_id: str, CMIP6Meta: dict) -> List[str]:
    """

    Args:
        activity_id: e.g. "CMIP", "ScenarioMIP"
        CMIP6Meta: Parsed JSON from CMIP6_source_id.json

    Returns:
        sil: List of source_id names that participate in the activity.
    """
    sil = []
    for source_id, meta in CMIP6Meta.get("source_id", {}).items():
        activities = meta.get("activity_participation", [])
        if activity_id in activities:
            sil.append(source_id)
    return sil


def load_cmip6_source_id(local_path: Optional[str]=None) -> dict:
    """
    Load CMIP6 source_id controlled vocabulary JSON. Tries local path first, then GitHub if not found.

    Args:
        local_path: Path to local CMIP6_source_id.json

    Returns:
        data: Parsed JSON content
    """
    url = "https://raw.githubusercontent.com/WCRP-CMIP/CMIP6_CVs/main/CMIP6_source_id.json"

    # Try local file first
    if local_path is not None and os.path.exists(local_path):
        with open(local_path) as f:
            data = json.load(f)
    else:
        with urllib.request.urlopen(url) as f:
            data = json.load(f)

    return data

def getModel_to_inst(CMIP6Meta: dict) -> dict:
    """
    Build a mapping from CMIP6 source_id (model name)
    to its first listed institution_id.

    Args:
        CMIP6Meta: Parsed JSON from CMIP6_source_id.json

    Returns:
        Dictionary of the form `{source_id: institution_id}`
    """
    return {
        source_id: (attrs.get("institution_id", [None])[0])
        for source_id, attrs in CMIP6Meta.get("source_id", {}).items()
    }

def checkCEDA(source_id: str, activity_id: str, experiment_id: str, M2I: dict, variableList: List[str],
              table_id: str, member_id: str = '*') -> pd.DataFrame:
    """
    For a given source_id (model), check which variables have data on CEDA,
    and return a DataFrame similar to intake-esm format, combining paths for identical metadata.

    Args:
        source_id: source_id (e.g. "MPI-ESM1-2-HR")
        activity_id: CMIP6 activity (e.g. "CMIP", "ScenarioMIP")
        experiment_id: Experiment (e.g. "historical", "ssp585")
        M2I: Mapping source_id -> institution_id (from getModel_to_inst)
        variableList: Variables to check (e.g. `['tas','rlut']`)
        table_id: Corresponding CMIP6 table_id e.g. 'Amon'
        member_id: The member Id specifically looked for - can be a wild car when searching for all members

    Returns:
        DataFrame with the following columns:</br>
            `['project', 'mip_era', 'activity_id', 'institution_id',
                  'source_id', 'experiment_id', 'member_id', 'table_id',
                  'variable_id', 'grid_label', 'version', 'id']`</br>
            Note that `'id'` contains a list of file paths for each unique combination of metadata.
    """
    inst = M2I.get(source_id)
    if inst is None:
        raise ValueError(f"No institution_id mapping found for source_id={SID}")

    records = []
    for variable in variableList:
        search_pattern = (
            f"/badc/cmip6/data/CMIP6/{activity_id}/"
            f"{inst}/{source_id}/{experiment_id}/{member_id}/"
            f"{table_id}/{variable}/*/latest/*.nc"
        )
        paths = glob.glob(search_pattern)
        if not paths:
            continue

        # Extract variant info
        variant_df = parse_variant_labels(paths)

        # Build record for each file
        for idx, row in variant_df.iterrows():
            records.append({
                "project": "CMIP6",
                "mip_era": "CMIP6",
                "activity_id": activity_id,
                "institution_id": inst,
                "source_id": source_id,
                "experiment_id": experiment_id,
                "member_id": row["member_id"],
                "table_id": table_id,
                "variable_id": variable,
                "grid_label": "gn",       # assuming native grid; could parse if needed
                "version": "latest",      # placeholder
                "id": row["path"]
            })

    df = pd.DataFrame(records)

    if not df.empty:
        # Combine rows with identical metadata except 'id' into a single row with list of ids
        group_cols = ['project', 'mip_era', 'activity_id', 'institution_id',
                      'source_id', 'experiment_id', 'member_id', 'table_id',
                      'variable_id', 'grid_label', 'version']
        df = df.groupby(group_cols, as_index=False)['id'].agg(list)

    return df

def checkESGF(source_id: str, activity_id: str, experiment_id: str, M2I: dict, variableList: List[str], table_id: str,
              member_id: str = '*') -> pd.DataFrame:
    """

    Args:
        source_id: source_id (e.g. "MPI-ESM1-2-HR")
        activity_id: CMIP6 activity (e.g. "CMIP", "ScenarioMIP")
        experiment_id: Experiment (e.g. "historical", "ssp585")
        M2I: Mapping source_id -> institution_id (from getModel_to_inst)
        variableList: Variables to check (e.g. `['tas','rlut']`)
        table_id: Corresponding CMIP6 table_id e.g. 'Amon'
        member_id: The member Id specifically looked for - can be a wild car when searching for all members

    Returns:
        DataFrame with the following columns:</br>
            `['project', 'mip_era', 'activity_id', 'institution_id',
                  'source_id', 'experiment_id', 'member_id', 'table_id',
                  'variable_id', 'grid_label', 'version', 'id']`</br>
            Note that `'id'` contains a list of file paths for each unique combination of metadata.
    """
    cat = initializeCat()
    if member_id == '*':
        cat.search(
            source_id=[source_id],
            activity_drs=[activity_id],
            experiment_id=[experiment_id],
            variable_id=variableList,
            table_id=table_id
        )
    else: 
        cat.search(
            source_id=[source_id],
            activity_drs=[activity_id],
            variant_label = [member_id],
            experiment_id=[experiment_id],
            variable_id=variableList,
            table_id=table_id
        )
    return cat

def parse_variant_labels(paths: List[str]) -> pd.DataFrame:
    """
    Given a list of CMIP6 file paths or variant_labels,
    extract r, i, p, f values into a DataFrame.

    Args:
        paths: CMIP6 file paths or strings containing a variant_label.

    Returns:
        DataFrame with columns `['member_id', 'r', 'i', 'p', 'f', 'path']`.

    Raises:
        ValueError: If any path/label does not contain a valid variant_id.
    """
    records = []
    for path in paths:
        match = re.search(r"(r\d+i\d+p\d+f\d+)", path)
        if not match:
            raise ValueError(f"No valid variant_label found in: {path}")
        variant = match.group(1)
        r, i, p, f = re.match(r"r(\d+)i(\d+)p(\d+)f(\d+)", variant).groups()
        records.append({"member_id": variant, "r": int(r), "i": int(i), "p": int(p), "f": int(f), "path": path})
    return pd.DataFrame(records)


def initializeCat() -> Optional[ESGFCatalog]:
    """
    Attempt to initialize an ESGFCatalog object with multiple retries.

    The function tries up to 20 times to create an ESGFCatalog instance,
    waiting a random interval between 15 and 60 seconds between attempts
    if initialization fails. This helps handle transient network or server issues.

    Returns:
        Successfully initialized ESGFCatalog object.

    Raises:
        RuntimeError: If the catalog cannot be initialized after 20 attempts.

    Notes:
        Each attempt logs its progress, and the exception is encountered if it fails.
    """
    import random
    import time
    for attempt in range(1, 21):
        try:
            print(f"Attempt {attempt} to initialize ESGFCatalog...")
            cat = ESGFCatalog()
            print("ESGFCatalog successfully initialized.")
            return cat  # success!
        except Exception as e:
            print(f"[Attempt {attempt}] ESGFCatalog failed to load: {e}")
            if attempt < 20:
                wait_time = random.randint(15, 60)
                print(f"Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                raise RuntimeError("Failed to initialize ESGFCatalog after multiple attempts.") from e


def compare_cat_res_pivot(cat_df: pd.DataFrame, res_df: pd.DataFrame) -> pd.DataFrame:
    """
    Compare two CMIP6 DataFrames (cat_df and res_df) and return a pivot table
    showing where each (member_id, variable_id) combination exists:
    'cat only', 'res only', or 'both'.

    If res_df is empty or missing required columns, bypass comparison and return
    a pivot table indicating all entries are from cat_df only.

    Args:
        cat_df: Catalog dataframe with columns `['member_id', 'variable_id']`
        res_df: Result dataframe with columns `['member_id', 'variable_id']`

    Returns:
        Pivot table: `index=member_id, columns=variable_id, values='cat only'/'res only'/'both'`
    """
    required_cols = {'member_id', 'variable_id'}
    
    # Check columns for cat_df
    missing_cat_cols = required_cols - set(cat_df.columns)
    if missing_cat_cols:
        raise KeyError(f"cat_df is missing columns: {missing_cat_cols}")

    # Bypass if res_df is empty or missing required columns
    missing_res_cols = required_cols - set(res_df.columns)
    if res_df.empty or missing_res_cols:
        print("Warning: res_df is empty or missing required columns. Marking all entries as 'ESGF_ONLY'")
        cat_set = set(cat_df[['member_id', 'variable_id']].itertuples(index=False, name=None))
        records = [{'member_id': k[0], 'variable_id': k[1], 'status': 'ESGF_ONLY'} for k in cat_set]
        df = pd.DataFrame(records)
        return df.pivot(index='member_id', columns='variable_id', values='status')

    # Proceed with normal comparison
    cat_set = set(cat_df[['member_id', 'variable_id']].itertuples(index=False, name=None))
    res_set = set(res_df[['member_id', 'variable_id']].itertuples(index=False, name=None))
    all_keys = cat_set | res_set
    
    records = []
    for key in all_keys:
        if key in cat_set and key in res_set:
            status = 'CEDA_CHOICE'
        elif key in cat_set:
            status = 'ESGF_ONLY'
        else:
            status = 'CEDA_ONLY'
        records.append({'member_id': key[0], 'variable_id': key[1], 'status': status})

    df = pd.DataFrame(records)
    return df.pivot(index='member_id', columns='variable_id', values='status')
    
def extract_r(member_id: str) -> int:
    """
    Extract `r<number>` from CMIP6 member_id string like `r1i1p1f1`.

    Args:
        member_id: The member id string e.g. `r1i1p1f1`

    Returns:
        The `number` where the `member_id` is in `r<number>` form.
    """
    m = re.match(r"r(\d+)i\d+p\d+f\d+", member_id)
    if not m:
        raise ValueError(f"Could not parse r-number from member_id: {member_id}")
    return int(m.group(1))



def rank_members_with_vars(pivot: pd.DataFrame) -> pd.DataFrame:
    """
    Rank member_ids by maximizing CEDA_CHOICE, minimizing ESGF_ONLY,
    then by r-number. Also attach the list of variable_ids available
    via CEDA and those only via ESGF.

    Args:
        pivot: Pivot table where rows correspond to `member_id` and columns
            correspond to `variable_id`. Each cell contains a status string indicating
            the availability of that variable for the member. Possible values include:

            - `"CEDA_CHOICE"`: Variable available via CEDA and preferred.
            - `"ESGF_ONLY"`: Variable only available via ESGF.
            - `"CEDA_ONLY"`: Variable only available via CEDA.

    Returns:
        A dataframe with one row per member containing (the dataframe is sorted descending by `CEDA_CHOICE_count`,
        ascending by `ESGF_ONLY_count`, and ascending by `r`):

            - `member_id`: The member identifier.
            - `CEDA_CHOICE_count`: Number of variables with status CEDA_CHOICE.
            - `ESGF_ONLY_count`: Number of variables with status ESGF_ONLY.
            - `CEDA_ONLY_count`: Number of variables with status CEDA_ONLY.
            - `CEDA_vars`: List of variable_ids available via CEDA (CEDA_CHOICE or CEDA_ONLY).
            - `ESGF_vars`: List of variable_ids available only via ESGF.
            - `r`: Extracted r-number from the member_id.
    """
    records = []
    for member_id, row in pivot.iterrows():
        # row is a Series: index = variable_id, value = status
        ceda_vars = row[row == "CEDA_CHOICE"].index.tolist()
        esgf_vars = row[row == "ESGF_ONLY"].index.tolist()
        ceda_only_vars = row[row == "CEDA_ONLY"].index.tolist()

        records.append({
            "member_id": member_id,
            "CEDA_CHOICE_count": len(ceda_vars),
            "ESGF_ONLY_count": len(esgf_vars),
            "CEDA_ONLY_count": len(ceda_only_vars),
            "CEDA_vars": ceda_vars,
            "ESGF_vars": esgf_vars,
            "r": extract_r(member_id),
        })

    df = pd.DataFrame(records)

    # Sort by: CEDA_CHOICE descending, ESGF_ONLY ascending, then r ascending
    df_sorted = df.sort_values(
        by=["CEDA_CHOICE_count", "ESGF_ONLY_count", "r"],
        ascending=[False, True, True]
    ).reset_index(drop=True)

    return df_sorted


def getCombinedData(source_id: str, activity_id: str, experiment_id: str, M2I: dict,
                    CEDA_vars: List[str], ESGF_vars: List[str], table_id: str, member_id: str,
                    doReadOut: bool = False) -> xr.Dataset:
    """

    Args:
        source_id: CMIP6 model/source ID (e.g., 'NorESM2-LM').
        activity_id: CMIP6 activity (e.g., 'DAMIP').
        experiment_id: CMIP6 experiment ID (e.g., 'hist-aer').
        M2I: Mapping from model variable names to CMOR variable names.
        CEDA_vars: Variables to retrieve from CEDA.
        ESGF_vars: Variables to retrieve from ESGF.
        table_id: CMIP6 table ID (e.g., 'Amon', 'Lmon').
        member_id: Variant label for the ensemble member (e.g., 'r1i1p1f1').
        doReadOut: Whether to print while loading or not

    Returns:
        Combined xarray Dataset containing requested variables from CEDA and ESGF.

            - If only CEDA_vars exist, returns CEDA dataset.
            - If only ESGF_vars exist, returns ESGF dataset.
            - If both exist, returns merged dataset.
    """
    ds = None  # placeholder

    if len(CEDA_vars) != 0:
        if doReadOut:
            print('loading CEDA Variables')
        CEDA_paths = checkCEDA(
            source_id, activity_id, experiment_id, M2I,
            CEDA_vars, table_id, member_id=member_id
        )
        CEDA_paths = sum(CEDA_paths["id"].tolist(), [])
        CEDA_ds = xr.open_mfdataset(CEDA_paths, combine='by_coords')
        ds = CEDA_ds

    if len(ESGF_vars) != 0:
        if doReadOut:
            print('loading ESGF Variables')
        ESGF_paths = checkESGF(
            source_id, activity_id, experiment_id, M2I,
            ESGF_vars, table_id, member_id=member_id
        )
        ESGF_ds = ESGF_paths.to_dataset_dict(add_measures=False, prefer_streaming=False)
        ESGF_ds = xr.merge([d for d in ESGF_ds.values()])
        ds = ESGF_ds if ds is None else xr.merge([ds, ESGF_ds], compat="override")

    return ds


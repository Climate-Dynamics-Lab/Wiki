# ERA5
The Climate Dynamics Lab maintains their own partial copy of daily and monthly mean ERA5 reanalysis data ([Hersbach et al. 2020](https://onlinelibrary.wiley.com/doi/abs/10.1002/qj.3803)) in zarr format. [Zarr](https://zarr.dev/) is a modern storage format, optimised for parallelized operations and efficient access. The data is stored in small chunks inside a folder structure which end users do not need to access manually (please don't try!). You can load and work with our ERA5 dataset in much the same way as you would with a netcdf file. This page details how to access the ERA5 dataset and what variables are currently available. 

## How to access the dataset

The dataset is stored in the data directory of our group workspace at `/gws/ssde/j25b/global_ex/data/`. To load and inspect the daily or monthly mean data as an xarray dataset, simply execute the following code snippets:

```python
import xarray as xr

path = "/gws/ssde/j25b/global_ex/data/"

d_daily = xr.open_zarr(
    path + "era5.zarr",
    chunks={}, 
    consolidated=True,
)

d_monthly = xr.open_zarr(
    path + "era5_monthly.zarr",
    chunks={}, 
    consolidated=True,
)
```


## Which variables are currently available?

- The current dataset covers the satellite era from 1979 to 2024.
- 2D variables are available globally, and 3D variables are available from the surface (1000hPa) up to 200hPa, corresponding to the lowest 23 pressure levels.
- For some variables, that haven't been actively used so far, only the metadata is included with the actual data defaulted to nan. Within the limits of our storage capacities, missing data or variables that are not yet included can be added easily upon request (contact Luca: lms47@st-andrews.ac.uk).
- Derived variables such as q2m and tw2m were computed from hourly data beform performing the daily averaging.

To see which variables contain meaningful data, run the following code snippet on your loaded daily or monthly dataset `d`:

```python
for var in d.data_vars:
    arr = d[var].isel(time=0, latitude = 0, longitude = 0).values
    if not np.isnan(arr).all():
        print(var)
```

## Error shooting

**Central differentiation:**

I had a bizarr case where I wanted to apply the central difference function `xarray.DataArray.differentiate()` to a certain derived variable (involving integration along levels), and got an error claiming that the chunk size of 10 was not suitable for `differentiate()`. While the reason for this behaviour remains opaque, it can be fixed efficiently by telling dask to treat each two consecutive chunks together by adding `.chunk(time = 20)` to the array before applying `differentiate()`. A minimal example for this solution reads:
```
ds['some_variable'].chunk(time = 20).differentiate('time')
```

Note though, that this problem does not present itself for any of the variables already included in `d_daily` or `d_monthly`, and also not for most derived variables.

from typing import Optional, Union
import numpy as np
import xarray as xr
from xarray import Dataset, DataArray
try:
    from xarray.core.weighted import DataArrayWeighted
except ModuleNotFoundError:
    from xarray.computation.weighted import DataArrayWeighted      # Version issue as to where DataArrayWeighted is


def area_weighting(var: xr.DataArray, weights: Optional[DataArray] = None) -> DataArrayWeighted:
    """
    Apply area weighting to the variable `var` using the `cosine` of latitude: $\cos (\phi)$.

    Args:
        var: Variable to weight e.g. `ds.t_surf` to weight the surface temperature, where
            `ds` is the dataset for the experiment which contains all variables.
        weights: Weights to use as a function of latitude. If not given, will just take cosine of latitude.

    Returns:
        Area weighted version of `var`.
    """
    if weights is None:
        weights = np.cos(np.deg2rad(var.lat))
        weights.name = "weights"
    return var.weighted(weights)


def lat_lon_coord_slice(ds: Dataset, lat: np.ndarray, lon: np.ndarray) -> Dataset:
    """
    Returns dataset, `ds`, keeping only data at the coordinate indicated by `(lat[i], lon[i])` for all `i`.

    If `ds` contained `t_surf` then the returned dataset would contain `t_surf` as a function of the variables
    `time` and `location` with each value of `location` corresponding to a specific `(lat, lon)` combination.
    For the original `ds`, it would be a function of `time`, `lat` and `lon`.

    This is inspired by a
    [stack overflow post](https://stackoverflow.com/questions/72179103/xarray-select-the-data-at-specific-x-and-y-coordinates).

    Args:
        ds: Dataset for a particular experiment.
        lat: `float [n_coords]`
            Latitude coordinates to keep.
        lon: `float [n_coords]`
            Longitude coordinates to keep.

    Returns:
        Dataset only including the desired coordinates.
    """
    # To get dataset at specific coordinates, not all permutations, turn to xarray first
    lat_xr = xr.DataArray(lat, dims=['location'])
    lon_xr = xr.DataArray(lon, dims=['location'])
    return ds.sel(lat=lat_xr, lon=lon_xr, method="nearest")


def area_weight_mean_lat(ds: Dataset) -> Dataset:
    """
    For all variables in `ds`, an area-weighted mean is taken over all latitudes in the dataset.

    Args:
        ds: Dataset for a particular experiment.

    Returns:
        Dataset containing averaged variables with no latitude dependence.
    """
    var_averaged = []
    for var in ds.keys():
        if 'lat' in list(ds[var].coords):
            ds[var] = area_weighting(ds[var]).mean(dim='lat')
            var_averaged += [var]
    print(f"Variables Averaged: {var_averaged}")
    return ds


def lat_lon_rolling(ds: Union[Dataset, DataArray], window_lat: int, window_lon: int) -> Union[Dataset, DataArray]:
    """
    This creates a rolling averaged version of the dataset or data-array in the spatial dimension.
    Returned data will have first `np.ceil((window_lat-1)/2)` and last `np.floor((window_lat-1)/2)`
    values as `nan` in latitude dimension.
    The averaging also does not take account of area weighting in latitude dimension.

    Args:
        ds: Dataset or DataArray to find rolling mean of.
        window_lat: Size of window for rolling average in latitude dimension [number of grid points]
        window_lon: Size of window for rolling average in longitude dimension [number of grid points].

    Returns:
        Rolling averaged dataset or DataArray.

    """
    ds_roll = ds.pad(lon=window_lon, mode='wrap')       # first pad in lon so wraps around when doing rolling mean
    ds_roll = ds_roll.rolling({'lon': window_lon, 'lat': window_lat}, center=True).mean()
    return ds_roll.isel(lon=slice(window_lon, -window_lon))     # remove the padded longitude values


def time_rolling(ds: Union[Dataset, DataArray], window_time: int, wrap: bool = True) -> Union[Dataset, DataArray]:
    """
    This creates a rolling-averaged version of the dataset or data-array in the time dimension. Useful for when
    you have an annual average dataset.

    Args:
        ds: Dataset or DataArray to find rolling mean of.
        window_time: Size of window for rolling average in time dimension [number of time units e.g. days]
        wrap: If the first time comes immediately after the last time i.e. for annual mean data

    Returns:
        Rolling averaged dataset or DataArray.
    """
    if wrap:
        ds_roll = ds.pad(time=window_time, mode='wrap')  # first pad in time so wraps around when doing rolling mean
        ds_roll = ds_roll.rolling(time=window_time, center=True).mean()
        return ds_roll.isel(time=slice(window_time, -window_time))  # remove the padded time values
    else:
        return ds.rolling(time=window_time, center=True).mean()

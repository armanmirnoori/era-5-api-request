import xarray as xr
from pathlib import Path

# 1) Gather all real extracted NetCDF files
files = sorted(Path(r"C:\Users\NAME\Desktop\ERA-5\extracted").rglob("*.nc"))
print("NetCDF files:", len(files))
print("Sample:", files[:3])

# 2) Combine all files along valid_time dimension
ds = xr.open_mfdataset(
    [str(f) for f in files],
    combine="nested",
    concat_dim="valid_time",
    engine="netcdf4",
    coords="minimal",
    data_vars="minimal",
    join="outer",
    compat="override",
)

# 3) Convert to a single Pandas DataFrame
df = ds.to_dataframe().reset_index()

print(df.head())
print("Rows:", len(df), "Cols:", len(df.columns))

# 4) Save the final merged DataFrame
df.to_parquet("era5_all.parquet", index=False)
df.to_csv("era5_all.csv", index=False)

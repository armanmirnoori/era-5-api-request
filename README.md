title: "ERA-5 Data Pipeline for WBGT"
description: >
  This repository provides a pipeline to download ERA-5 climate data,
  extract ZIP-encoded .nc archives, merge NetCDF slices using xarray + dask,
  and convert them into a single DataFrame for WBGT heat-stress index calculation.
steps:
  - "Create .cdsapirc in C:\\Users\\<YOUR_USERNAME>\\.cdsapirc and add: url + key"
  - "Edit main.py and replace file location, year, and month"
  - "main.py downloads .nc files which are ZIP internally"
  - "Run extract_all.py with correct absolute pathing to generate extracted NetCDF files"
  - "Run view.py to merge extracted .nc files and export a single CSV/Parquet for WBGT"
output:
  csv: "era5_all.csv"
  parquet: "era5_all.parquet"

variables_used_for_wbgt:
  - "t2m — 2m air temperature (Kelvin)"
  - "d2m — 2m dew point temperature (Kelvin)"
  - "u10, v10 — 10m wind components (m/s)"
  - "ssrd — surface solar radiation"

execution_order_commands: |
  python main.py
  python extract_all.py
  python view.py

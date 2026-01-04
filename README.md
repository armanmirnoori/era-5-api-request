# ERA-5 Data Retrieval for WBGT Pipeline

This repository includes Python scripts to download, extract, merge, and convert ERA-5 climate data for **WBGT (Wet Bulb Globe Temperature) calculation**, used for heat-stress and environmental analysis.

---

## Setup

1. **Create the CDS API credentials file at:  C:\Users<YOUR_USERNAME>.cdsapirc**
2. Add:  url: https://cds.climate.copernicus.eu/api
         key: <YOUR_API_KEY>
   in the cdsapirc file

3.Update dataset parameters in main.py
**Replace**:
file location path
year
month
data needed from era-5
"File format inside the generated folder is ZIP archives named .nc."

4.Extract the archives
Run **extract.py** to unpack ZIP-disguised .nc files into the extracted/ directory.

5.Convert merged data to DataFrame
Run **view.py** after extraction.
This script merges all real extracted NetCDF files using xarray + dask, converts them into a single Pandas DataFrame, and exports:
era5_all.csv
era5_all.parquet

Author
Arman Mirnoori

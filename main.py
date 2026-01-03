"""
ERA-5 Data Fetcher and WBGT Calculator
Fetches meteorological data from ERA-5 and calculates Wet Bulb Globe Temperature (WBGT)
"""

import cdsapi
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

# CDS API credentials - User needs to set these
# CDS_UID = os.getenv('CDS_UID', 'https://cds...')  # Your CDS user ID
# CDS_KEY = os.getenv('CDS_KEY', 'a467347...')  # Your CDS API key
AREA = [24.517896729052016, 55.50607141349063, 24.017896729052016, 56.00607141349063] #add your own location

def fetch_era5_data(year, month, variables, output_file):
    """
    Fetch ERA-5 reanalysis data from CDS
    
    Parameters:
    -----------
    year : int
        Year to fetch data for
    month : int
        Month to fetch data for
    variables : list
        List of variable names to fetch
    output_file : str
        Output file path for downloaded data
    """
    c = cdsapi.Client() #need to have .cdsapirs file in your C://USER/NAME/...
    
    c.retrieve(
        'reanalysis-era5-single-levels',
        {
            'product_type': 'reanalysis',
            'variable': variables,
            'year': str(year),
            'month': f'{month:02d}',
            'day': [f'{day:02d}' for day in range(1, 32)],
            'time': [f'{hour:02d}:00' for hour in range(24)],
            'area': AREA,
            'format': 'netcdf',
        },
        output_file
    )

def calculate_wbgt(temp_2m, dewpoint_2m, u10, v10, ssrd):
    """
    Calculate Wet Bulb Globe Temperature (WBGT) from ERA-5 data
    
    Parameters:
    -----------
    temp_2m : array
        2-meter air temperature (K)
    dewpoint_2m : array
        2-meter dewpoint temperature (K)
    u10 : array
        10-meter u-component of wind (m/s)
    v10 : array
        10-meter v-component of wind (m/s)
    ssrd : array
        Surface solar radiation downwards (J/m²)
    
    Returns:
    --------
    wbgt : array
        Wet Bulb Globe Temperature (°C)
    """
    # Convert temperature from Kelvin to Celsius
    temp_c = temp_2m - 273.15
    dewpoint_c = dewpoint_2m - 273.15
    
    # Calculate relative humidity
    # Using simplified formula: RH = 100 * exp((17.625 * Td) / (243.04 + Td) - (17.625 * T) / (243.04 + T))
    rh = 100 * np.exp((17.625 * dewpoint_c) / (243.04 + dewpoint_c) - 
                      (17.625 * temp_c) / (243.04 + temp_c))
    
    # Calculate wind speed from u and v components
    wind_speed = np.sqrt(u10**2 + v10**2)
    
    # Calculate natural wet bulb temperature (Tw)
    # Simplified approximation using temperature and humidity
    tw = temp_c * np.arctan(0.151977 * np.sqrt(rh + 8.313659)) + \
         np.arctan(temp_c + rh) - np.arctan(rh - 1.676331) + \
         0.00391838 * (rh**(3/2)) * np.arctan(0.023101 * rh) - 4.686035
    
    # Estimate globe temperature (Tg) from solar radiation
    # Convert solar radiation from J/m² to W/m² (assuming hourly data)
    solar_flux = ssrd / 3600  # Convert J/m² to W/m² for hourly data
    
    # Simplified globe temperature estimation
    # Tg depends on solar radiation, air temperature, and wind
    tg = temp_c + (solar_flux / (wind_speed + 0.1)) * 0.01
    
    # Calculate WBGT using the standard formula
    # WBGT = 0.7*Tw + 0.2*Tg + 0.1*Ta
    wbgt = 0.7 * tw + 0.2 * tg + 0.1 * temp_c
    
    return wbgt, temp_c, rh, wind_speed

def process_era5_data(nc_file, output_csv):
    """
    Process downloaded ERA-5 NetCDF file and calculate WBGT
    
    Parameters:
    -----------
    nc_file : str
        Path to NetCDF file
    output_csv : str
        Path to output CSV file
    """
    import xarray as xr
    
    # Load NetCDF file
    ds = xr.open_dataset(nc_file)
    
    # Extract variables
    temp_2m = ds['t2m'].values
    dewpoint_2m = ds['d2m'].values
    u10 = ds['u10'].values
    v10 = ds['v10'].values
    ssrd = ds['ssrd'].values
    
    # Calculate WBGT
    wbgt, temp_c, rh, wind_speed = calculate_wbgt(
        temp_2m, dewpoint_2m, u10, v10, ssrd
    )
    
    # Get coordinates
    times = ds['time'].values
    lats = ds['latitude'].values
    lons = ds['longitude'].values
    
    # Create DataFrame
    data_list = []
    for t_idx, time in enumerate(times):
        for lat_idx, lat in enumerate(lats):
            for lon_idx, lon in enumerate(lons):
                data_list.append({
                    'datetime': pd.to_datetime(str(time)),
                    'latitude': float(lat),
                    'longitude': float(lon),
                    'temperature_2m_c': float(temp_c[t_idx, lat_idx, lon_idx]),
                    'dewpoint_2m_c': float(dewpoint_2m[t_idx, lat_idx, lon_idx] - 273.15),
                    'relative_humidity': float(rh[t_idx, lat_idx, lon_idx]),
                    'wind_speed_ms': float(wind_speed[t_idx, lat_idx, lon_idx]),
                    'solar_radiation_wm2': float(ssrd[t_idx, lat_idx, lon_idx] / 3600),
                    'wbgt_c': float(wbgt[t_idx, lat_idx, lon_idx])
                })
    
    df = pd.DataFrame(data_list)
    
    # Save to CSV
    df.to_csv(output_csv, index=False)
    print(f"Data saved to {output_csv}")
    print(f"Total records: {len(df)}")
    
    ds.close()
    return df

def main():
    """
    Main function to fetch ERA-5 data and calculate WBGT from 2022 to 2025
    """
    # Check credentials
    # if not CDS_UID or not CDS_KEY:
    #     print("ERROR: CDS credentials not found!")
    #     print("Please set environment variables:")
    #     print("  CDS_UID: Your Copernicus CDS user ID")
    #     print("  CDS_KEY: Your Copernicus CDS API key")
    #     print("\nOr edit main.py and set CDS_UID and CDS_KEY directly")
    #     print("\nGet your credentials from: https://cds.climate.copernicus.eu/user")
    #     return
    
    # Variables needed for WBGT calculation
    print("CWD:", os.getcwd())
    print("Output dir (abs):", os.path.abspath("output"))
    print("Era5 dir (abs):", os.path.abspath("era5_data"))

    variables = [
        '2m_temperature',
        '2m_dewpoint_temperature',
        '10m_u_component_of_wind',
        '10m_v_component_of_wind',
        'surface_solar_radiation_downwards'
    ]
    
    # Create output directory
    os.makedirs('era5_data', exist_ok=True)
    os.makedirs('output', exist_ok=True)
    
    all_dataframes = []
    
    # Fetch data for each year and month
    for year in range(2022, 2023):  # 2022 to 2025
        for month in range(1, 3):
            print(f"\nFetching data for {year}-{month:02d}...")
            
            nc_file = f'era5_data/era5_{year}_{month:02d}.nc'
            csv_file = f'output/wbgt_{year}_{month:02d}.csv'
            
            try:
                # Fetch data from CDS
                if not os.path.exists(nc_file):
                    print(f"Downloading ERA-5 data...")
                    fetch_era5_data(year, month, variables, nc_file)
                else:
                    print(f"Using existing file: {nc_file}")
                
                # Process and calculate WBGT
                print(f"Processing data and calculating WBGT...")
                df = process_era5_data(nc_file, csv_file)
                all_dataframes.append(df)
                
            except Exception as e:
                print(f"Error processing {year}-{month:02d}: {str(e)}")
                continue
    
    # Combine all dataframes
    if all_dataframes:
        print("\nCombining all data...")
        combined_df = pd.concat(all_dataframes, ignore_index=True)
        
        # Sort by datetime
        combined_df = combined_df.sort_values(['datetime', 'latitude', 'longitude'])
        
        # Save combined CSV
        output_file = 'output/wbgt_2022_2025.csv'
        combined_df.to_csv(output_file, index=False)
        print(f"\nAll data saved to {output_file}")
        print(f"Total records: {len(combined_df)}")
        print(f"Date range: {combined_df['datetime'].min()} to {combined_df['datetime'].max()}")
        print(f"\nFirst few rows:")
        print(combined_df.head())

if __name__ == "__main__":
    main()

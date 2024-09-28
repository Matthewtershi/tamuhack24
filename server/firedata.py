from datetime import datetime, timedelta
from pathlib import Path
import requests
from netCDF4 import Dataset
from bisect import bisect

BASE_URL = "https://portal.nccs.nasa.gov/datashare/GlobalFWI/v2.0/fwiCalcs.GEOS-5/Default/GEOS-5"

def current_data_filename():
    yesterday = datetime.now() - timedelta(1)
    yyyymmdd = yesterday.strftime("%Y%m%d")
    yyyymmdd_today = datetime.now().strftime("%Y%m%d")
    return f"FWI.GEOS-5.Daily.Default.{yyyymmdd}00.{yyyymmdd_today}.nc"

def current_data_uri():
    yesterday = datetime.now() - timedelta(1)
    yyyy = yesterday.strftime("%Y")
    yyyymmdd = yesterday.strftime("%Y%m%d")
    return f"{BASE_URL}/{yyyy}/{yyyymmdd}00/{current_data_filename()}"

def get_lat_long_idx(data, lat, long):
    lat_idx = bisect(data.variables["lat"], lat)
    long_idx = bisect(data.variables["lon"], long)

    return lat_idx, long_idx

def get_ffmc(data, lat_idx, long_idx):
    return data.variables["GEOS-5_FFMC"][0][lat_idx][long_idx]

def get_dmc(data, lat_idx, long_idx):
    return data.variables["GEOS-5_DMC"][0][lat_idx][long_idx]

def get_dc(data, lat_idx, long_idx):
    return data.variables["GEOS-5_DC"][0][lat_idx][long_idx]

def get_isi(data, lat_idx, long_idx):
    return data.variables["GEOS-5_ISI"][0][lat_idx][long_idx]

if __name__ == "__main__":
    data_path = Path("./data/") / current_data_filename()
    if not data_path.exists():
        print(f"Downloading data for {data_path}")
        req = requests.get(current_data_uri())
        
        req.raise_for_status()

        with open(data_path, "wb") as f:
            f.write(req.content)
    
    rootgrp = Dataset(data_path, "r")
    lat_idx, long_idx = get_lat_long_idx(rootgrp, 30.601433, -96.314464)

    print(get_ffmc(rootgrp, lat_idx, long_idx))

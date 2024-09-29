from datetime import datetime, timedelta
from io import BytesIO
from pathlib import Path
import requests
from netCDF4 import Dataset
from bisect import bisect
import gzip
import shutil
import math
import numpy as np
import threading

import grib2io

BASE_FWI_URL = "https://portal.nccs.nasa.gov/datashare/GlobalFWI/v2.0/fwiCalcs.GEOS-5/Default/GEOS-5"
BASE_RAIN_URL = "https://opendata.dwd.de/climate_environment/GPCC/first_guess/"

EARTH_RADIUS = 6371e4

class DataSource:
    def __init__(self):
        self.lock = threading.Lock()
    
    def update(self):
        pass
    
    def delete_old(self):
        pass

    def get_data(self, lat, long):
        pass

class FWIData(DataSource):
    def __init__(self):
        super().__init__()

        self.fwi_data_path = Path("./data/") / FWIData._current_fwi_filename()

        with self.lock:
            self.update()
            self.delete_old()
    
    def update(self):
        if not self.fwi_data_path.exists():
            print(f"Downloading data for {self.fwi_data_path}")
            req = requests.get(FWIData._current_fwi_uri())
            
            req.raise_for_status()

            with open(self.fwi_data_path, "wb") as f:
                f.write(req.content)
        
        self.data = Dataset(self.fwi_data_path, "r")
    
    def delete_old(self):
        for file in Path("./data/").glob("FWI.GEOS-5.Daily.Default.*"):
            if file.name == FWIData._current_fwi_filename():
                continue
            file.unlink()
    
    def get_data(self, lat, long):
        lat_idx = bisect(self.data.variables["lat"], lat)
        long_idx = bisect(self.data.variables["lon"], long)

        return {
            "FFMC": self.data.variables["GEOS-5_FFMC"][0][lat_idx][long_idx],
            "DMC": self.data.variables["GEOS-5_DMC"][0][lat_idx][long_idx],
            "DC": self.data.variables["GEOS-5_DC"][0][lat_idx][long_idx],
            "ISI": self.data.variables["GEOS-5_ISI"][0][lat_idx][long_idx]
        }

    @staticmethod
    def _current_fwi_filename():
        yesterday = datetime.now() - timedelta(2)
        yyyymmdd = yesterday.strftime("%Y%m%d")
        yyyymmdd_today = datetime.now().strftime("%Y%m%d")
        return f"FWI.GEOS-5.Daily.Default.{yyyymmdd}00.{yyyymmdd_today}.nc"
    
    @staticmethod
    def _current_fwi_uri():
        yesterday = datetime.now() - timedelta(2)
        return yesterday.strftime(f"{BASE_FWI_URL}/%Y/%Y%m%d00/{FWIData._current_fwi_filename()}")
    
class RainData(DataSource):
    def __init__(self):
        super().__init__()

        self._rain_data_path = Path("./data/") / self._current_rain_filename(compressed=False)

        with self.lock:
            self.update()
            self.delete_old()

    def update(self):
        if not self._rain_data_path.exists():
            print(f"Downloading rain data for {self._current_fwi_uri()}")
            req = requests.get(self._current_rain_uri())
            req.raise_for_status()

            with open(self._rain_data_path, "wb") as f:
                data = gzip.decompress(req.content)
                f.write(data)
    
        self.data = Dataset(self._rain_data_path, "r")
    
    def get_data(self, lat, long):
        closest_lat = min(self.data.variables["lat"], key=lambda x: abs(x - lat))
        closest_long = min(self.data.variables["lon"], key=lambda x: abs(x - long))

        lat_idx = list(self.data.variables["lat"]).index(closest_lat)
        long_idx = list(self.data.variables["lon"]).index(closest_long)


        latitude = self.data.variables["lat"][lat_idx]
        cell_area = math.sin(latitude * math.pi / 180) - math.sin((latitude - 1) * math.pi / 180) * math.pi/180 * EARTH_RADIUS**2
        cell_area = abs(cell_area)

        return self.data.variables["p"][0][lat_idx][long_idx] / cell_area / 30

    @staticmethod
    def _current_rain_filename(compressed = True):
        last_month = datetime.now() - timedelta(days=31)
        return last_month.strftime(f"first_guess_monthly_%Y_%m.nc{'.gz' if compressed else ''}")

    @staticmethod
    def _current_rain_uri():
        return datetime.now().strftime(f"{BASE_RAIN_URL}/%Y/{RainData._current_rain_filename()}")

class WindData(DataSource):
    def __init__(self):
        super().__init__()

        with self.lock:
            self.update()
    
    def update(self):
        self.grib = grib2io.open("data/gfs.t00z.pgrb2.1p00.f000") # TODO: Update
        self.lats, self.lons = self.grib[0].grid()
        self.lats = self.lats.transpose()

        self.speeds = np.sqrt(self.grib[0].data**2 + self.grib[1].data**2)
    
    def get_data(self, lat, long):
        lat_idx = np.abs(self.lats - lat).argmin()
        lon_idx = np.abs(self.lons - (180-long)).argmin()

        return self.speeds[lat_idx][lon_idx]

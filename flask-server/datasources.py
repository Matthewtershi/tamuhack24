from datetime import datetime, timedelta
from io import BytesIO
from pathlib import Path
import requests
from netCDF4 import Dataset
from bisect import bisect
import gzip
import math
import numpy as np
import threading

import grib2io

from herbie import Herbie

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

    def delete_old(self):
        for file in Path("./data/").glob("first_guess_monthly_*"):
            if file.name == RainData._current_rain_filename(compressed=False):
                continue
            file.unlink()
    
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

class GFSData(DataSource):
    def __init__(self):
        super().__init__()

        with self.lock:
            self.update()
    
    def update(self):
        yesterday = datetime.now() - timedelta(1)
        self.H = Herbie(yesterday.strftime("%Y-%m-%d"), model="gfs")
        path = self.H.download(r":[U|V]GRD:10 m above|:TMP:2 m above|:RH:2 m above")

        self.grib = grib2io.open(path)
        self.tmp = self.grib.select(shortName='TMP')[0]
        self.rh = self.grib.select(shortName="RH")[0]
        self.ugrd = self.grib.select(shortName="UGRD")[0]
        self.vgrd = self.grib.select(shortName="VGRD")[0]
        self.speeds = np.sqrt(self.ugrd.data**2 + self.vgrd.data**2)

        self.tmp_lats, self.tmp_lons = self.tmp.grid()
        self.tmp_lats = self.tmp_lats.transpose()[0]
        self.tmp_lons = self.tmp_lons[0]

        self.rh_lats, self.rh_lons = self.rh.grid()
        self.rh_lats = self.rh_lats.transpose()[0]
        self.rh_lons = self.rh_lons[0]

        self.speed_lats, self.speed_lons = self.ugrd.grid()
        self.speed_lats = self.speed_lats.transpose()[0]
        self.speed_lons = self.speed_lons[0]

    def get_data(self, lat, long):
        tmp_lat_idx = np.abs(self.tmp_lats - lat).argmin()
        tmp_lon_idx = np.abs(self.tmp_lons - (180-long)).argmin()

        rh_lat_idx = np.abs(self.rh_lats - lat).argmin()
        rh_lon_idx = np.abs(self.rh_lons - (180-long)).argmin()

        speed_lat_idx = np.abs(self.speed_lats - lat).argmin()
        speed_lon_idx = np.abs(self.speed_lons - (180-long)).argmin()

        return self.tmp[tmp_lat_idx][tmp_lon_idx], self.rh[rh_lat_idx][rh_lon_idx], self.speeds[speed_lat_idx][speed_lon_idx]

class DataSources:
    def __init__(self):
        self.FWI = FWIData()
        self.Rain = RainData()
        self.GFS = GFSData()

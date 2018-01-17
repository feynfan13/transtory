"""
Mobike trip logging functionality
"""
import pandas as pd
from datetime import datetime, date, time

from .configs import logger

from .dbops import MobikeDbOps, get_mobike_db_ops
from .dbops import MobikeSysConfigs, get_configs
from .dbops import DateTimeHelper, get_datetime_helper
from .dbops import TripEntry


class XlsxLogEntry(object):
    def __init__(self, sr_entry):
        self.date = sr_entry["Date"].to_pydatetime()
        self.time = sr_entry["Time"]
        assert(isinstance(self.time, time))
        self.city = sr_entry["City"].strip()
        self.departure_region = self._strip_if_not_none(sr_entry["Departure Area"])
        self.departure_place = self._strip_if_not_none(sr_entry["Departure Place"])
        self.departure_coordinate = self._strip_if_not_none(sr_entry["Departure Coord"])
        self.arrival_region = self._strip_if_not_none(sr_entry["Arrival Area"])
        self.arrival_place = self._strip_if_not_none(sr_entry["Arrival Place"])
        self.arrival_coordinate = self._strip_if_not_none(sr_entry["Arrival Coord"])
        self.bike_sn = self._strip_if_not_none(sr_entry["Bike SN"])
        self.bike_type = self._strip_if_not_none(sr_entry["Bike Type"])
        self.bike_subtype = self._cast_if_not_none(sr_entry["Bike Subtype"], int)
        self.duration = self._cast_if_not_none(sr_entry["Duration"], int)
        self.distance = self._cast_if_not_none(sr_entry["Distance"], float)
        self.trip_note = self._strip_if_not_none(sr_entry["Trip Comment"])
        self.bike_note = self._strip_if_not_none(sr_entry["Bike Comment"])

    @staticmethod
    def _strip_if_not_none(val: str):
        return None if pd.isnull(val) else val.strip()

    @staticmethod
    def _value_if_not_none(val):
        return None if pd.isnull(val) else val

    @staticmethod
    def _cast_if_not_none(val, atype: type):
        return None if pd.isnull(val) else atype(val)

    def generate_trip_entry(self):
        entry = TripEntry()
        entry.city = self.city
        dt_helper: DateTimeHelper = get_datetime_helper()
        entry.time = dt_helper.get_datetime_from_date_time(self.date, self.time)
        entry.departure_region = self.departure_region
        entry.departure_place = self.departure_place
        entry.departure_coordinate = self.departure_coordinate
        entry.arrival_region = self.arrival_region
        entry.arrival_place = self.arrival_place
        entry.arrival_coordinate = self.arrival_coordinate
        entry.duration = self.duration
        entry.distance = self.distance
        entry.trip_note = self.trip_note
        entry.bike_sn = self.bike_sn
        if self.bike_type is None or self.bike_type == "":
            entry.bike_subtype = "NA"
        else:
            if self.bike_subtype is None:
                entry.bike_subtype = self.bike_type[0:-1] + "x"
            else:
                entry.bike_subtype = self.bike_type[0:-1] + "{:d}".format(self.bike_subtype)
        entry.bike_note = self.bike_note
        return entry


class MobikeRecorder(object):
    """The class is to handle information flow from the excel table to database
    The class has the following use cases:
      -- Record: Input the trip record in the excel table into database
      -- Update: Compare the trip record in database with the corresponding one in excel table.
            If the record in table is updated, merge update into database
    """
    def __init__(self):
        self.configs: MobikeSysConfigs = get_configs()
        self.db_ops: MobikeDbOps = get_mobike_db_ops()
        self.dt_helper: DateTimeHelper = get_datetime_helper()

    def record_trips_from_xlsx(self):
        """Record new trips in trip excel table to database
        TODO: when the excel table become big
          -- read from multiple excel tables
          -- read the excel table in batch mode
        """
        trip_df: pd.DataFrame = pd.read_excel(self.configs.trip_xlsx_path, converters={"Bike SN": str})
        for trip_idx, trip_row in trip_df.iterrows():
            log_entry = XlsxLogEntry(trip_row)
            trip_entry = log_entry.generate_trip_entry()
            if self.db_ops.get_trip(trip_entry) is None:
                self.db_ops.add_trip(trip_entry)
                logger.info("Added trip at {:s}".format(self.dt_helper.get_datetime_str(trip_entry.time)))
            else:
                logger.info("Skip trip at {:s}".format(self.dt_helper.get_datetime_str(trip_entry.time)))
            pass

    def update_trips_from_xlsx(self):
        """Update the database by comparing with entries in trip excel table.
        WARNING: This function may take long.
        """
        trip_df: pd.DataFrame = pd.read_excel(self.configs.trip_xlsx_path, converters={"Bike SN": str})
        for trip_idx, trip_row in trip_df.iterrows():
            log_entry = XlsxLogEntry(trip_row)
            trip_entry = log_entry.generate_trip_entry()
            trip_orm = self.db_ops.get_trip(trip_entry)
            if trip_orm is None:
                self.db_ops.add_trip(trip_entry)
                logger.info("Added trip at {:s}".format(self.dt_helper.get_datetime_str(trip_entry.time)))
            else:
                trip_updated = self.db_ops.update_trip(trip_orm, trip_entry)
                if trip_updated:
                    logger.info("Updated trip at {:s}".format(self.dt_helper.get_datetime_str(trip_entry.time)))
                else:
                    logger.info("Skipped trip at {:s}".format(self.dt_helper.get_datetime_str(trip_entry.time)))
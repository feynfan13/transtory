from datetime import time
import pandas as pd

from transtory.common import DateTimeHelper

from .configs import get_configs, ShmSysConfigs
from .configs import get_datetime_helper
from .dbops import get_shm_db_ops, ShmDbOps
from .dbops import InputRouteEntry


class XlsxLogEntry(object):
    def __init__(self, sr_trip):
        dt_helper: DateTimeHelper = get_datetime_helper()
        self.task = self._strip_if_not_none(sr_trip["Task"])
        self.date = dt_helper.get_date_from_str(self._strip_if_not_none(sr_trip["Date"]))
        self.line = int(sr_trip["Line"])
        train_sn = self._strip_if_not_none(sr_trip["Train SN"])
        # To accomodate both the old 4-digit format and new 5-digit format
        if len(train_sn) == 4:
            train_sn = "{:02d}{:03d}".format(int(train_sn[:2]), int(train_sn[2:]))
        assert(len(train_sn) == 5)
        self.train_sn = train_sn
        assert(not pd.isnull(sr_trip["Departure Station"]))
        self.departure_station = self._strip_if_not_none(sr_trip["Departure Station"])
        self.departure_time = dt_helper.get_time_from_str(self._strip_if_not_none(sr_trip["Departure Time"]))
        assert(not pd.isnull(sr_trip["Arrival Station"]))
        self.arrival_station = self._strip_if_not_none(sr_trip["Arrival Station"])
        self.arrival_time = dt_helper.get_time_from_str(self._strip_if_not_none(sr_trip["Arrival Time"]))
        self.trip_note = self._strip_if_not_none(sr_trip["Trip Note"])

    def make_route_entry(self):
        entry = InputRouteEntry()
        entry.task = self.task
        entry.line = self.line
        entry.date = self.date
        entry.train_sn = self.train_sn
        entry.departure_station = self.departure_station
        entry.departure_time = self.departure_time
        entry.arrival_station = self.arrival_station
        entry.arrival_time = self.arrival_time
        entry.trip_note = self.trip_note
        return entry

    @staticmethod
    def _strip_if_not_none(val: str):
        return None if pd.isnull(val) else val.strip().strip("|")

    @staticmethod
    def _value_if_not_none(val):
        return None if pd.isnull(val) else val

    @staticmethod
    def _cast_if_not_none(val, atype: type):
        return None if pd.isnull(val) else atype(val)


class ShmRecorder(object):
    def __init__(self):
        self.configs: ShmSysConfigs = get_configs()
        self.db_ops: ShmDbOps = get_shm_db_ops()
        self.dt_helper: DateTimeHelper = get_datetime_helper()

    def record_trips_from_xlsx(self):
        trip_df: pd.DataFrame = pd.read_excel(self.configs.trip_xlsx_path, converters={"Train SN": str})
        for trip_idx, trip_row in trip_df.iterrows():
            log_entry = XlsxLogEntry(trip_row)
            entry = log_entry.make_route_entry()
            self.db_ops.add_route(entry)

    def update_trips_from_xlsx(self):
        # TODO: add update functionality for shanghaimetro recorder
        pass

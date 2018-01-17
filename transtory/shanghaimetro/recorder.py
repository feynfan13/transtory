from datetime import time
import pandas as pd

from transtory.common import DateTimeHelper

from .configs import get_configs, ShmSysConfigs
from .configs import get_datetime_helper
from .dbops import get_shm_db_ops, ShmDbOps
from .dbops import TrainEntry, RouteEntry


class XlsxLogEntry(object):
    def __init__(self, sr_trip):
        self.task = self._strip_if_not_none(sr_trip["Task"])
        self.date = sr_trip["Date"].to_pydatetime()
        self.line = "Line {:2d}".format(int(sr_trip["Line"]))
        self.train_sn = self._strip_if_not_none(sr_trip["Train SN"])
        assert(not pd.isnull(sr_trip["Departure Station"]))
        self.departure_station = self._strip_if_not_none(sr_trip["Departure Station"])
        assert(isinstance(sr_trip["Departure Time"], time))
        self.departure_time = sr_trip["Departure Time"]
        assert(not pd.isnull(sr_trip["Arrival Station"]))
        self.arrival_station = self._strip_if_not_none(sr_trip["Arrival Station"])
        assert (isinstance(sr_trip["Arrival Time"], time))
        self.arrival_time = sr_trip["Arrival Time"]
        self.trip_note = self._strip_if_not_none(sr_trip["Trip Note"])

    @staticmethod
    def _strip_if_not_none(val: str):
        return None if pd.isnull(val) else val.strip()

    @staticmethod
    def _value_if_not_none(val):
        return None if pd.isnull(val) else val

    @staticmethod
    def _cast_if_not_none(val, atype: type):
        return None if pd.isnull(val) else atype(val)

    def generate_route_entry(self):
        dt_helper: DateTimeHelper = get_datetime_helper()
        configs: ShmSysConfigs = get_configs()
        entry = RouteEntry()
        entry.task = self.task
        entry.train = self.train_sn
        entry.departure_station = self.departure_station
        departure_datetime = dt_helper.get_datetime_from_date_time(self.date, self.departure_time)
        entry.departure_time = dt_helper.get_utc_datetime(departure_datetime, configs.city)
        entry.arrival_station = self.arrival_station
        arrival_datetime = dt_helper.get_datetime_from_date_time(self.date, self.arrival_time)
        entry.arrival_time = dt_helper.get_utc_datetime(arrival_datetime, configs.city)
        entry.note = self.trip_note
        return entry


class ShmRecorder(object):
    def __init__(self):
        self.configs: ShmSysConfigs = get_configs()
        self.db_ops: ShmDbOps = get_shm_db_ops()
        self.dt_helper: DateTimeHelper = get_datetime_helper()

    def record_trips_from_xlsx(self):
        trip_df: pd.DataFrame = pd.read_excel(self.configs.trip_xlsx_path, converters={"Train SN": str})
        for trip_idx, trip_row in trip_df.iterrows():
            log_entry = XlsxLogEntry(trip_row)
            entry = log_entry.generate_route_entry()
            if self.db_ops.get_route(entry) is None:
                self.db_ops.add_route(entry)

    def update_trips_from_xlsx(self):
        # TODO: add update functionality for shanghaimetro recorder
        pass

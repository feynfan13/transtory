from datetime import time
import pandas as pd

from transtory.common import DateTimeHelper

from .configs import get_configs, ShmSysConfigs
from .configs import get_datetime_helper
from .dbops import get_shm_db_ops, ShmDbOps


class XlsxLogEntry(object):
    def __init__(self, sr_trip):
        self.task = None if pd.isnull(sr_trip["Task"]) else sr_trip["Task"].strip()
        self.date = sr_trip["Date"].to_pydatetime()
        self.line = "Line {:2d}".format(sr_trip["Line"])
        self.train_sn = None if pd.isnull(sr_trip["Train SN"]) else sr_trip["Train SN"].strip()
        assert(not pd.isnull(sr_trip["Departure Station"]))
        self.departure_station = sr_trip["Departure Station"].strip()
        assert(isinstance(sr_trip["Departure Time"], time))
        self.departure_time = sr_trip["Departure Time"]
        assert(not pd.isnull(sr_trip["Arrival Station"]))
        self.arrival_station = sr_trip["Arrival Station"].strip()
        assert (isinstance(sr_trip["Arrival Time"], time))
        self.arrival_time = sr_trip["Arrival Time"]
        self.trip_note = None if pd.isnull(sr_trip["Trip Note"]) else sr_trip["Trip Note"].strip()


class ShmRecorder(object):
    def __init__(self):
        self.configs: ShmSysConfigs = get_configs()
        self.db_ops: ShmDbOps = get_shm_db_ops()
        self.dt_helper: DateTimeHelper = get_datetime_helper()

    def record_trips_from_xlsx(self):
        trip_df: pd.DataFrame = pd.read_excel(self.configs.trip_xlsx_path, converters={"Train SN": str})
        for trip_idx, trip_row in trip_df.iterrows():
            entry = XlsxLogEntry(trip_row)
            route_id = self.db_ops.get_route_id_from_date_time_str(entry.date, entry.departure_time)
            if not self.db_ops.is_route_exist(route_id):
                self.db_ops.insert_route(entry)

    def update_trips_from_xlsx(self):
        pass

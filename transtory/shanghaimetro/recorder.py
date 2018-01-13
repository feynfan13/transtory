from datetime import time
import pandas as pd

from transtory.common import DateTimeHelper

from .configs import get_configs, ShmSysConfigs
from .configs import get_datetime_helper


class LogTripEntry(object):
    def __init__(self, sr_trip):
        self.task = sr_trip["Task"].strip()
        self.date = sr_trip["Date"].to_pydatetime()
        self.line = "Line {:2d}".format(sr_trip["Line"])
        self.train_sn = sr_trip["Train SN"].strip()
        self.depart_station = sr_trip["Departure Station"].strip()
        assert(isinstance(sr_trip["Departure Time"], time))
        self.depart_time = sr_trip["Departure Time"]
        self.arrive_station = sr_trip["Arrival Station"].strip()
        assert (isinstance(sr_trip["Arrival Time"], time))
        self.arrive_time = sr_trip["Arrival Time"]
        self.trip_note = None if pd.isnull(sr_trip["Trip Note"]) else sr_trip["Trip Note"].strip()


class ShmRecorder(object):
    def __init__(self):
        self.configs: ShmSysConfigs = get_configs()
        # self.db_ops: MobikeDbOps = get_mobike_db_ops()
        self.dt_helper: DateTimeHelper = get_datetime_helper()

    def record_trips_from_xlsx(self):
        trip_df: pd.DataFrame = pd.read_excel(self.configs.trip_xlsx_path, converters={"Train SN": str})
        for trip_idx, trip_row in trip_df.iterrows():
            entry = LogTripEntry(trip_row)
            pass

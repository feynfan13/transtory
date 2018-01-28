from datetime import time
import pandas as pd

from transtory.common import DateTimeHelper

from .configs import get_configs, CrhSysConfigs
from .configs import get_datetime_helper
from .dbops import get_db_ops, CrhDbOps
from .dbops import InputTripEntry


class XmlLogEntry(object):
    def __init__(self):
        pass

    def make_trip_entry(self):
        pass


class CrhRecorder(object):
    def __init__(self):
        self.configs: CrhSysConfigs = get_configs()
        self.db_ops: CrhDbOps = get_db_ops()
        self.dt_helper: DateTimeHelper = get_datetime_helper()

    def record_trips_from_xmls(self):
        trip_df: pd.DataFrame = pd.read_excel(self.configs.trip_xlsx_path, converters={"Train SN": str})
        for trip_idx, trip_row in trip_df.iterrows():
            log_entry = XmlLogEntry(trip_row)
            entry = log_entry.make_trip_entry()
            self.db_ops.add_route(entry)

    def update_trips_from_xmls(self):
        # TODO: add update functionality for shanghaimetro recorder
        pass
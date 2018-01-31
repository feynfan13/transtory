from .configs import FlightSysConfigs, get_configs
from .dbops import FlightDbOps, get_db_ops
from .dbops import DateTimeHelper, get_datetime_helper


class XmlLogEntry(object):
    def __init__(self):
        pass

    def make_trip_entry(self):
        pass


class FlightRecorder(object):
    def __init__(self):
        self.configs: FlightSysConfigs = get_configs()
        self.db_ops: FlightDbOps = get_db_ops()
        self.dt_helper: DateTimeHelper = get_datetime_helper()

    def record_trips_from_xmls(self):
        pass
        # trip_df: pd.DataFrame = pd.read_excel(self.configs.trip_xlsx_path, converters={"Train SN": str})
        # for trip_idx, trip_row in trip_df.iterrows():
        #     log_entry = XmlLogEntry(trip_row)
        #     entry = log_entry.make_trip_entry()
        #     self.db_ops.add_route(entry)

    def update_trips_from_xmls(self):
        # TODO: add update functionality for shanghaimetro recorder
        pass
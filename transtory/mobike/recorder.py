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


class MobikeRecorderTransTable(object):
    """Infrastructure for Mobike trip recorder.
    The intention is, if the relation between excel file and database is changed,
      only this class needs to be changed to accomodate.
    """
    def __init__(self):
        self.db_ops: MobikeDbOps = get_mobike_db_ops()
        self.dt_ops: DateTimeHelper = get_datetime_helper()
        self.excel_to_inter = self._def_excel_to_inter_table()
        self.inter_to_orm = self._def_inter_to_orm_table()

    @staticmethod
    def _def_excel_to_inter_table():
        """Define converter from excel table to a clean internal structure
        """
        trans_table = [
            # database column name, excel columns of data source, transform function
            ["Date", "departure_date", lambda x: x.to_pydatetime()],
            ["Time", "departure_clock", lambda x: x],
            ["City", "city", lambda x: x],
            ["Departure Area", "departure_region", lambda x: None if pd.isnull(x) else x.strip()],
            ["Departure Place", "departure_place", lambda x: None if pd.isnull(x) else x.strip()],
            ["Departure Coord", "departure_coordinate", lambda x: None if pd.isnull(x) else x.strip()],
            ["Arrival Area", "arrival_region", lambda x: None if pd.isnull(x) else x.strip()],
            ["Arrival Place", "arrival_place", lambda x: None if pd.isnull(x) else x.strip()],
            ["Arrival Coord", "arrival_coordinate", lambda x: None if pd.isnull(x) else x.strip()],
            ["Bike SN", "bike_sn", lambda x: x],
            ["Bike Type", "bike_type", lambda x: None if pd.isnull(x) else x.strip()],
            ["Bike Subtype", "bike_subtype", lambda x: None if pd.isnull(x) else x],
            ["Duration", "trip_duration", lambda x: int(x)],
            ["Distance", "trip_distance", lambda x: float(x)],
            ["Trip Comment", "trip_note", lambda x: None if pd.isnull(x) else x.strip()],
            ["Bike Comment", "bike_service_note", lambda x: None if pd.isnull(x) else x.strip()]
        ]
        return trans_table

    def _def_inter_to_orm_table(self):
        """Define converter from internal structure to db data
        """
        trans_table = []
        # trip_id
        trip_id_item = ["trip_id", ["departure_date", "departure_clock"],
                        lambda x, y: self.db_ops.get_trip_id_from_date_time(x, y)]
        trans_table.append(trip_id_item)
        # departure_time
        departure_time_item = ["departure_time", ["departure_date", "departure_clock"],
                               lambda x, y: self.dt_ops.get_date_str(x) + " " + self.dt_ops.get_time_str(y)]
        trans_table.append(departure_time_item)
        # bike_subtype_name

        def _get_bike_subtype_name(type_name, subtype_num):
            if type_name is None or type_name == "":
                return "NA"
            else:
                if subtype_num is None:
                    return type_name[0:-1]+"x"
                else:
                    return type_name[0:-1]+"{:d}".format(int(subtype_num))

        bike_subtype_name_item = ["bike_subtype_name", ["bike_type", "bike_subtype"],
                                  _get_bike_subtype_name]
        trans_table.append(bike_subtype_name_item)
        # Directly transform
        direct_used_items = ["city", "departure_region", "departure_place", "departure_coordinate",
                             "arrival_region", "arrival_place", "arrival_coordinate", "trip_duration",
                             "trip_distance", "trip_note", "bike_sn", "bike_service_note"]
        for item in direct_used_items:
            trans_table.append([item, [item], lambda x: None if x == "" else x])
        return trans_table


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
        self.trans_table = MobikeRecorderTransTable()

    def _read_xlsx_record_to_internal(self, record_sr):
        trans_table = self.trans_table.excel_to_inter
        trip_inter = dict()
        for field_desc in trans_table:
            trip_inter[field_desc[1]] = field_desc[2](record_sr[field_desc[0]])
        return trip_inter

    def _read_internal_to_orm(self, trip_sr):
        trans_table = self.trans_table.inter_to_orm
        trip_orm = dict()
        for field_desc in trans_table:
            param_list = [trip_sr[name] for name in field_desc[1]]
            trip_orm[field_desc[0]] = field_desc[2](*param_list)
        return trip_orm

    def record_trips_from_xlsx(self):
        """Log the trip excel table into memory as pandas DataFrame.
        It acts as the "data cleaning" function.
        TODO: when the excel table become big
          -- read from multiple excel tables
          -- read the excel table in batch mode
        """
        trip_df: pd.DataFrame = pd.read_excel(self.configs.trip_xlsx_path, converters={"Bike SN": str})
        for trip_idx, trip_row in trip_df.iterrows():
            # trip_inter = self._read_xlsx_record_to_internal(trip_row)
            # trip_dict = self._read_internal_to_orm(trip_inter)
            log_entry = XlsxLogEntry(trip_row)
            trip_entry = log_entry.generate_trip_entry()
            if self.db_ops.get_trip(trip_entry) is None:
                self.db_ops.add_trip(trip_entry)
                logger.info("Added trip at {:s}".format(self.dt_helper.get_datetime_str(trip_entry.time)))
            else:
                logger.info("Skip trip at {:s}".format(self.dt_helper.get_datetime_str(trip_entry.time)))
            pass

    def update_trips_from_xlsx(self):
        # TODO: add update functionality to mobike trip recorder
        pass

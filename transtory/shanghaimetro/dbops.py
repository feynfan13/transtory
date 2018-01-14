from transtory.common import DatabaseOpsBase, singleton
from transtory.common import DateTimeHelper

from .configs import get_datetime_helper
from .configs import logger
from .configs import ShmSysConfigs, get_configs

from .dbdefs import ShmDbModel, Train, Line, Station
from .dbdefs import Task, Route, Departure, Arrival


class ShmDbOps(DatabaseOpsBase):
    def __init__(self):
        self.configs: ShmSysConfigs = get_configs()
        self.dt_helper: DateTimeHelper = get_datetime_helper()
        # super(ShmDbOps, self).__init__(self.configs.db_path, self.configs.test_mode)
        super(ShmDbOps, self).__init__(self.configs.db_path, False)
        logger.info("Created ShmDbOps instance.")

    def create_db_structure(self):
        logger.info("Creating shanghai metro database structure.")
        ShmDbModel.metadata.create_all(bind=self.engine)

    # Method type: transforming input data to database data
    def get_trip_id_from_date_time_str(self, date_str, time_str):
        date_int = self.dt_helper.get_date_int_from_date_str(date_str)
        time_int = self.dt_helper.get_time_int_from_time_str(time_str)
        return date_int * 24 * 60 + time_int

    def get_trip_id_from_date_time(self, date, time):
        date_int = self.dt_helper.get_date_int(date)
        time_int = self.dt_helper.get_time_int(time)
        return date_int * 24 * 60 + time_int


get_shm_db_ops = singleton(ShmDbOps)

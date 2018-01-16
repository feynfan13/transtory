from transtory.common import DatabaseOpsBase, singleton
from transtory.common import DateTimeHelper

from .configs import get_datetime_helper
from .configs import logger
from .configs import ShmSysConfigs, get_configs

from .dbdefs import ShmDbModel, TrainType, Train, Line, Station, Task, Route, Departure, Arrival


class TrainEntry(object):
    def __init__(self):
        self.id = None
        self.sn = None
        self.line = None
        self.type = None


class RouteEntry(object):
    def __init__(self):
        self.id = None
        self.task = None
        self.train = None
        self.departure_station = None
        self.departure_date = None
        self.departure_time = None
        self.arrival_station = None
        self.arrival_time = None
        self.note = None


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
    def get_route_id_from_date_time_str(self, date_str, time_str):
        date_int = self.dt_helper.get_date_int_from_date_str(date_str)
        time_int = self.dt_helper.get_time_int_from_time_str(time_str)
        return date_int * 24 * 60 + time_int

    def get_route_id_from_date_time(self, date, time):
        date_int = self.dt_helper.get_date_int(date)
        time_int = self.dt_helper.get_time_int(time)
        return date_int * 24 * 60 + time_int

    def get_train_type(self, train_type):
        return self.session.query(TrainType).filter_by(name=train_type).one()

    def get_line(self, line):
        return self.session.query(Line).filter_by(name=line).one()

    def is_train_exist(self, train_sn):
        query = self.session.query(Train).filter_by(sn=train_sn)
        return query.count() == 1

    def insert_train(self, train_entry: TrainEntry):
        train = Train()
        train.id = train_entry.id
        train.sn = train_entry.sn
        train.line = self.get_line(train_entry.line)
        train.train_type = self.get_train_type(train_entry.type)
        logger.info("Inserted train {:s}".format(repr(train)))

    def get_train(self, train_sn):
        return self.session.query(Train).filter_by(sn=train_sn).one

    def is_route_exist(self, route_id):
        query = self.session.query(Route).filter_by(id=route_id)
        return query.count() == 1

    def insert_route(self, route_entry: RouteEntry):
        pass


get_shm_db_ops = singleton(ShmDbOps)

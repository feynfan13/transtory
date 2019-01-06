from pytz import timezone

from transtory.common import DatabaseOpsBase, singleton
from transtory.common import DateTimeHelper

from .configs import get_datetime_helper
from .configs import logger
from .configs import ShmSysConfigs, get_configs
from .publicdata import ShmPublicDataApp, get_public_data_app

from .dbdefs import ShmDbModel, TrainType, Train, Line, Station, Task, Route, Departure, Arrival


class InputRouteEntry(object):
    """Data interface class between log entry and RouteDbEntry.
    The class is the 1st layer of the two-layer structure from external data to database data.
    The members of the class matches the external data; their values should be conveniently transformed to database
        values.
    This class should be released to (known by) external codes, such as recorder
    """
    def __init__(self):
        self.task = None
        self.line = None
        self.train_sn = None
        self.date = None
        self.departure_station = None
        self.departure_time = None
        self.arrival_station = None
        self.arrival_time = None
        self.note = None


class RouteEntry(object):
    """Data interface class between database and RouteEntry.
    The class should accept data from RouteEntry. The data it holds should match exactly with the database values.
    The only difference is the field name, as the class can hold data from multiple tables.
    This class is hidden from external codes, such as recorder, which help hide the database fields.
    """
    def __init__(self):
        self.task = None
        self.train_sn = None
        self.departure_station = None
        self.departure_time = None
        self.arrival_station = None
        self.arrival_time = None
        self.note = None

    def get_data_from_input_route_entry(self, entry: InputRouteEntry):
        dt_helper: DateTimeHelper = get_datetime_helper()
        configs: ShmSysConfigs = get_configs()
        self.task = entry.task
        self.line = entry.line
        self.train_sn = entry.train_sn
        self.departure_station = entry.departure_station
        adatetime = dt_helper.get_datetime_from_date_time(entry.date, entry.departure_time)
        self.departure_time = dt_helper.get_datetime_str(dt_helper.get_utc_datetime(adatetime, configs.city))
        self.arrival_station = entry.arrival_station
        adatetime = dt_helper.get_datetime_from_date_time(entry.date, entry.arrival_time)
        self.arrival_time = dt_helper.get_datetime_str(dt_helper.get_utc_datetime(adatetime, configs.city))
        self.note = entry.note


class TrainEntry(object):
    def __init__(self):
        self.id = None
        self.sn = None
        self.line = None
        self.type = None


class ShmDbOps(DatabaseOpsBase):
    def __init__(self):
        self.configs: ShmSysConfigs = get_configs()
        self.dt_helper: DateTimeHelper = get_datetime_helper()
        self.data_app: ShmPublicDataApp = get_public_data_app()
        # super(ShmDbOps, self).__init__(self.configs.db_path, self.configs.test_mode)
        super(ShmDbOps, self).__init__(self.configs.db_path, False)
        logger.info("Created ShmDbOps instance.")

    def create_db_structure(self):
        logger.info("Creating shanghai metro database structure.")
        ShmDbModel.metadata.create_all(bind=self.engine)

    @staticmethod
    def get_line_name_from_num(line_num):
        assert(isinstance(line_num, int))
        return "Line {:02d}".format(line_num)

    def get_local_time_from_db_time(self, entry_time_list):
        atz = self.dt_helper.get_time_zone_of_city(self.configs.city)
        local_time_list = []
        for entry_time in entry_time_list:
            adt = self.dt_helper.get_datetime_from_str(entry_time)
            adt = adt.replace(tzinfo=timezone("UTC"))
            local_datetime = adt.astimezone(atz)
            local_time_list.append(self.dt_helper.get_datetime_str(local_datetime))
        return local_time_list

    def _get_task(self, task):
        query = self.session.query(Task).filter_by(task=task)
        return None if query.count() == 0 else query.one()

    def _add_task(self, task):
        task_orm = Task()
        task_orm.task = task
        self.session.add(task_orm)
        return task_orm

    def _get_train_type(self, train_type):
        return self.session.query(TrainType).filter_by(name=train_type).one()

    def _get_station(self, line_name, chn_name):
        query = self.session.query(Station, Line).join(Station.line)
        query = query.filter(Station.chn_name == chn_name).filter(Line.codename == line_name)
        return query.one()[0]

    def _get_line(self, line):
        return self.session.query(Line).filter_by(codename=line).one()

    def _get_train(self, train_sn):
        query = self.session.query(Train).filter_by(sn=train_sn)
        return None if query.count() == 0 else query.one()

    def _add_train(self, train_entry: TrainEntry):
        train_orm = Train()
        train_orm.id = train_entry.id
        train_orm.sn = train_entry.sn
        train_orm.line = self._get_line(train_entry.line)
        train_orm.train_type = self._get_train_type(train_entry.type)
        logger.info("Added train {:s}".format(train_entry.sn))
        self.session.commit()
        return train_orm

    def _get_route(self, route_entry: RouteEntry):
        query = self.session.query(Route, Departure).join(Route.departure).filter_by(time=route_entry.departure_time)
        return None if query.count() == 0 else query.one()[0]

    def _add_route(self, entry: RouteEntry):
        task_orm = self._get_task(entry.task)  # For task
        if task_orm is None:
            task_orm = self._add_task(entry.task)
        if 'xx' in entry.train_sn:
            train_orm = None
        else:
            train_orm = self._get_train(entry.train_sn)  # For train
            if train_orm is None:
                train_entry = TrainEntry()
                train_entry.sn = entry.train_sn
                # line, seq = self.data_app.get_line_and_seq_from_train_sn(train_entry.sn)
                train_entry.type = self.data_app.get_type_of_train(train_entry.sn)
                train_entry.line = entry.line
                train_orm = self._add_train(train_entry)
        departure_orm = Departure()  # For departure
        departure_orm.station = self._get_station(entry.line, entry.departure_station)
        departure_orm.time = entry.departure_time
        arrival_orm = Arrival()  # For arrival
        arrival_orm.station = self._get_station(entry.line, entry.arrival_station)
        arrival_orm.time = entry.arrival_time
        route_orm = Route()
        route_orm.task = task_orm
        route_orm.departure = departure_orm
        route_orm.arrival = arrival_orm
        route_orm.train = train_orm
        route_orm.note = entry.note
        self.session.add(departure_orm)
        self.session.add(arrival_orm)
        self.session.add(route_orm)
        self.session.commit()
        return route_orm

    def add_route(self, input_entry: InputRouteEntry):
        route_entry = RouteEntry()
        route_entry.get_data_from_input_route_entry(input_entry)
        route_orm = self._get_route(route_entry)
        if route_orm is None:
            route_orm = self._add_route(route_entry)
            logger.info("Added route at {:s}.".format(route_orm.departure.time))
        else:
            logger.info("Route exist at {:s}.".format(route_orm.departure.time))

    def update_route(self, entry: InputRouteEntry):
        # TODO: update_route is not frequently used; implementation is postponed
        pass


get_shm_db_ops = singleton(ShmDbOps)

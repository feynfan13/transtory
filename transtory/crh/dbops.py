from transtory.common import DatabaseOpsBase, singleton
from transtory.common import DateTimeHelper

from .configs import get_datetime_helper
from .configs import logger
from .configs import CrhSysConfigs, get_configs

from .publicdata import CrhPublicDataApp, get_public_data_app
from .dbdefs import CrhDbModel, Task, Trip, Route, Departure, Arrival, Ticket
from .dbdefs import Line, LineStart, LineFinal, Station
from .dbdefs import Train, TrainType, TrainService


class InputTripEntry(object):
    def __init__(self):
        self.task = None
        self.train_num = None
        self.train_num_start = None
        self.train_num_final = None
        self.ticket_short_sn = None
        self.ticket_long_sn = None
        self.price = None
        self.ticket_sold_by = None
        self.ticket_sold_type = None
        self.seat_type = None
        self.seat_num = None
        self.note = None
        self.routes = list()


class InputRouteEntry(object):
    def __int__(self):
        self.seat_train = None
        self.join_train = None
        self.join_type = None
        # 0 for forward position; 1 for backward position
        self.seat_train_pos = None
        self.carriage = None
        self.note = None
        self.start = None
        self.start_time, self.start_time_schedule = None, None
        self.start_gate, self.start_platform = None, None
        self.start_note = None
        self.final = None
        self.final_time, self.final_time_schedule = None, None
        self.final_platform, self.final_gate = None, None
        self.final_note = None


class CrhDbOps(DatabaseOpsBase):
    """Operations of CRH database, including
    """
    def __init__(self):
        self.configs: CrhSysConfigs = get_configs()
        self.data_app: CrhPublicDataApp = get_public_data_app()
        self.dt_helper: DateTimeHelper = get_datetime_helper()
        self.data_app: CrhPublicDataApp = get_public_data_app()
        super(CrhDbOps, self).__init__(self.configs.db_path)
        logger.info("Created CrhDbOps instance.")

    def create_db_structure(self):
        """Create or validate database structure
        """
        logger.info("Creating CRH database structure.")
        CrhDbModel.metadata.create_all(bind=self.engine)

    def _get_task(self, content):
        query = self.session.query(Task).filter_by(content=content)
        if query.count() == 0:
            return None
        return query.one()

    def _add_task(self, content):
        task_orm = Task()
        task_orm.content = content
        self.session.add(task_orm)
        return task_orm

    def get_or_add_task(self, content):
        task_orm = self._get_task(content)
        if task_orm is None:
            task_orm = self._add_task(content)
        return task_orm

    def _get_station(self, chn_name):
        query = self.session.query(Station).filter_by(chn_name=chn_name)
        if query.count() == 0:
            return None
        return query.one()

    def _add_station(self, chn_name):
        station_orm = Station()
        station_orm.chn_name = chn_name
        self.session.add(station_orm)
        logger.info("Added station ", station_orm.chn_name)
        return station_orm

    def get_or_add_station(self, chn_name):
        station_orm = self._get_station(chn_name)
        if station_orm is None:
            station_orm = self._add_station(chn_name)
        return station_orm

    def _get_line(self, line_num, start, final):
        lines = self.session.query(Line).filter_by(name=line_num).all()
        for line in lines:
            start_orm, final_orm = line.start, line.final
            if start_orm.station.chn_name == start and final_orm.station.chn_name == final:
                return line
        return None

    def _add_line(self, line, start, final):
        start_station_orm = self._get_station(start)
        if start_station_orm is None:
            start_station_orm = self._add_station(start)
        end_station_orm = self._get_station(final)
        if end_station_orm is None:
            end_station_orm = self._add_station(final)
        line_start_orm = LineStart()
        line_start_orm.station = start_station_orm
        line_final_orm = LineFinal()
        line_final_orm.station = end_station_orm
        line_orm = Line()
        line_orm.name = line
        line_orm.start = line_start_orm
        line_orm.final = line_final_orm
        self.session.add(line_orm)
        logger.info("Added line {:s} from {:s} to {:s}".format(line, start, final))
        return line_orm

    def get_or_add_line(self, line, start, final):
        line_orm = self._get_line(line, start, final)
        if line_orm is None:
            line_orm = self._add_line(line, start, final)
        return line_orm

    def _get_train_type(self, train_type):
        query = self.session.query(TrainType).filter_by(name=train_type)
        return query.one()

    def _get_train(self, train_sn):
        query = self.session.query(Train).filter_by(sn=train_sn)
        if query.count() == 0:
            return None
        return query.one()

    def _add_train(self, train_sn):
        train_orm = Train()
        train_orm.sn = train_sn
        train_type = self.data_app.get_train_type(train_sn)
        train_orm.type = self._get_train_type(train_type)
        self.session.add(train_orm)
        logger.info("Added train {:s}".format(train_sn))
        return train_orm

    def get_or_add_train(self, train_sn):
        train_orm = self._get_train(train_sn)
        if train_orm is None:
            train_orm = self._add_train(train_sn)
        return train_orm

    def _add_route(self, route_entry: InputRouteEntry, trip_orm: Trip):
        route_orm = Route()
        route_orm.trip = trip_orm
        seat_train_orm = self.get_or_add_train(route_entry.seat_train)
        train_service_orm = TrainService()
        train_service_orm.route = route_orm
        train_service_orm.train = seat_train_orm
        train_service_orm.operation_type = 0
        self.session.add(train_service_orm)
        if route_entry.join_train is not None:
            join_train_orm = self.get_or_add_train(route_entry.join_train)
            train_service_orm = TrainService()
            train_service_orm.route = route_orm
            train_service_orm.train = join_train_orm
            train_service_orm.operation_type = route_entry.join_type
            self.session.add(train_service_orm)
        route_orm.carriage = route_entry.carriage
        route_orm.note = route_entry.note
        departure_orm = Departure()
        departure_orm.time = route_entry.start_time
        departure_orm.planned_time = route_entry.start_time_schedule
        departure_orm.station = self.get_or_add_station(route_entry.start)
        departure_orm.gate = route_entry.start_gate
        departure_orm.platform = route_entry.start_platform
        departure_orm.note = route_entry.start_note
        self.session.add(departure_orm)
        route_orm.departure = departure_orm
        arrival_orm = Arrival()
        arrival_orm.time = route_entry.final_time
        arrival_orm.planned_time = route_entry.final_time_schedule
        arrival_orm.station = self.get_or_add_station(route_entry.final)
        arrival_orm.gate = route_entry.final_gate
        arrival_orm.platform = route_entry.final_platform
        arrival_orm.note = route_entry.final_note
        self.session.add(arrival_orm)
        route_orm.arrival = arrival_orm
        self.session.add(route_orm)
        return route_orm

    @staticmethod
    def _is_valid_ticket(trip_entry: InputTripEntry):
        is_invalid = True
        is_invalid = is_invalid and (trip_entry.ticket_short_sn is None)
        is_invalid = is_invalid and (trip_entry.ticket_long_sn is None)
        is_invalid = is_invalid and (trip_entry.ticket_sold_type is None)
        is_invalid = is_invalid and (trip_entry.ticket_sold_by is None)
        return not is_invalid

    def _add_trip(self, trip_entry: InputTripEntry):
        trip_orm = Trip()
        trip_orm.task = self.get_or_add_task(trip_entry.task)
        trip_orm.line = self.get_or_add_line(trip_entry.train_num, trip_entry.train_num_start,
                                             trip_entry.train_num_final)
        trip_orm.seat_type = trip_entry.seat_type
        trip_orm.seat_number = trip_entry.seat_num
        trip_orm.price = trip_entry.price
        trip_orm.note = trip_entry.note
        if self._is_valid_ticket(trip_entry):
            ticket_orm = Ticket()
            ticket_orm.short_sn = trip_entry.ticket_short_sn
            ticket_orm.long_sn = trip_entry.ticket_long_sn
            ticket_orm.sold_type = trip_entry.ticket_sold_type
            ticket_orm.sold_by = trip_entry.ticket_sold_by
            ticket_orm.trip = trip_orm
            self.session.add(ticket_orm)
        for route_entry in trip_entry.routes:
            self._add_route(route_entry, trip_orm)
        return trip_orm

    def add_trip(self, trip_entry: InputTripEntry):
        self._add_trip(trip_entry)
        self.session.commit()
        return True


get_db_ops = singleton(CrhDbOps)

from pytz import timezone

from transtory.common import DatabaseOpsBase, singleton
from transtory.common import DateTimeHelper

from .configs import get_datetime_helper
from .configs import logger
from .configs import FlightSysConfigs, get_configs

from .publicdata import FlightPublicDataApp, get_public_data_app

from .dbdefs import FlightDbModel, Trip, Route, Leg, Departure, Arrival
from .dbdefs import Flight, Airline, Airport, Plane, PlaneModel


class InputTripEntry(object):
    def __init__(self):
        self.confirmation_num = None
        self.price = None
        self.segments = []


class InputRouteEntry(object):
    def __init__(self):
        self.segment_seq = None
        self.segment_type = None
        self.status = None
        self.flight = None
        self.e_ticket_num = None
        self.cabin = None
        self.seat = None
        self.fare_code = None
        self.boarding_group = None
        self.plane = None
        self.plane_model = None
        self.miles_from_FA = None
        self.legs = []


class InputLegEntry(object):
    def __init__(self):
        self.leg_seq = None
        self.leg_type = None
        self.start_airport = None
        self.start_terminal = None
        self.start_concourse = None
        self.start_gate = None
        self.takeoff_runway = None
        self.pushback_time_FA = None
        self.pushback_time_planned_FA = None
        self.takeoff_time_FA = None
        self.takeoff_time_planned_FA = None
        self.departure_time_FR24 = None
        self.departure_time_planned_FR24 = None
        self.final_airport = None
        self.final_terminal = None
        self.final_concourse = None
        self.final_gate = None
        self.landing_runway = None
        self.landing_time_FA = None
        self.landing_time_planned_FA = None
        self.gate_arrival_time_FA = None
        self.gate_arrival_time_planned_FA = None
        self.arrival_time_FR24 = None
        self.arrival_time_planned_FR24 = None


class FlightDbOps(DatabaseOpsBase):
    """Operations of CRH database, including
    """
    def __init__(self):
        self.configs: FlightSysConfigs = get_configs()
        self.data_app: FlightPublicDataApp = get_public_data_app()
        self.dt_helper: DateTimeHelper = get_datetime_helper()
        super(FlightDbOps, self).__init__(self.configs.db_path)
        logger.info("Created FlightDbOps instance.")

    def create_db_structure(self):
        """Create or validate database structure
        """
        logger.info("Creating flight database structure.")
        FlightDbModel.metadata.create_all(bind=self.engine)

    def get_flight_num(self, flight_orm: Flight):
        return flight_orm.airline.iata + flight_orm.number

    def get_local_time_from_db_time(self, atime_str, city):
        atz = self.dt_helper.get_time_zone_of_city(city)
        adt = self.dt_helper.get_datetime_from_str(atime_str)
        adt = adt.replace(tzinfo=timezone("UTC"))
        return self.dt_helper.get_datetime_str(adt.astimezone(atz))

    def get_db_time_from_local_time(self, atime_str, city):
        adt = self.dt_helper.get_datetime_from_str(atime_str)
        adt = self.dt_helper.get_utc_datetime(adt, city)
        return self.dt_helper.get_datetime_str(adt)

    @staticmethod
    def get_airline_and_num_from_flight(flight_num):
        return flight_num[0:2], flight_num[2:]

    def get_airline(self, airline_iata):
        query = self.session.query(Airline).filter_by(iata=airline_iata)
        if query.count() == 0:
            return None
        return query.one()

    def add_airline(self, airline_iata):
        airline_orm = Airline()
        airline_orm.iata = airline_iata
        self.session.add(airline_orm)
        return airline_orm

    def get_or_add_airline(self, airline_iata):
        airline_orm = self.get_airline(airline_iata)
        if airline_orm is None:
            airline_orm = self.add_airline(airline_iata)
        return airline_orm

    def get_plane_model(self, plane_model):
        query = self.session.query(PlaneModel).filter_by(name=plane_model)
        return query.one()

    def add_plane(self, tail_num, plane_model, airline_id):
        plane_orm = Plane()
        plane_model_orm = self.get_plane_model(plane_model)
        plane_orm.tail_number = tail_num
        plane_orm.model = plane_model_orm
        plane_orm.airline_id = airline_id
        self.session.add(plane_orm)
        return plane_orm

    def get_plane(self, tail_num):
        query = self.session.query(Plane).filter_by(tail_number=tail_num)
        if query.count() == 0:
            return None
        return query.one()

    def get_or_add_plane(self, tail_num, plane_model, airline_id):
        plane_orm = self.get_plane(tail_num)
        if plane_orm is None:
            plane_orm = self.add_plane(tail_num, plane_model, airline_id)
        return plane_orm

    def get_airport(self, airport_iata):
        query = self.session.query(Airport).filter_by(iata=airport_iata)
        if query.count() == 0:
            return None
        return query.one()

    def add_airport(self, airport_iata):
        airport_orm = Airport()
        airport_orm.iata = airport_iata
        self.session.add(airport_orm)
        return airport_orm

    def get_or_add_airport(self, airport_iata):
        airport_orm = self.get_airport(airport_iata)
        if airport_orm is None:
            raise ValueError("Airport {:s} does not exist in database, causing missing city info.".format(airport_iata))
            airport_orm = self.add_airport(airport_iata)
        return airport_orm

    def get_flight(self, flight_num):
        query = self.session.query(Flight).filter_by(number=flight_num)
        if query.count() == 0:
            return None
        return query.one()

    def add_flight(self, flight):
        flight_orm = Flight()
        airline_iata, flight_num = self.get_airline_and_num_from_flight(flight)
        flight_orm.number = flight_num
        airline_orm = self.get_airline(airline_iata)
        flight_orm.airline = airline_orm
        self.session.add(flight_orm)
        return flight_orm

    def get_or_add_flight(self, flight_num):
        flight_orm = self.get_flight(flight_num)
        if flight_orm is None:
            flight_orm = self.add_flight(flight_num)
        return flight_orm

    def add_leg(self, leg_entry: InputLegEntry, route_orm: Route):
        leg_orm = Leg()
        leg_orm.seq = leg_entry.leg_seq
        leg_orm.type = leg_entry.leg_type
        leg_orm.route = route_orm
        departure_orm = Departure()
        airport_orm = self.get_or_add_airport(leg_entry.start_airport)
        departure_orm.airport = airport_orm
        departure_orm.gate = leg_entry.start_gate
        departure_orm.concourse = leg_entry.start_concourse
        departure_orm.terminal = leg_entry.start_terminal
        departure_orm.runway = leg_entry.takeoff_runway
        airport_city = airport_orm.city
        departure_times = {"pushback_time": "pushback_time_FA",
                           "planned_pushback_time": "pushback_time_planned_FA",
                           "takeoff_time": "takeoff_time_FA",
                           "planned_takeoff_time": "takeoff_time_planned_FA"}
        for orm_field, input_field in departure_times.items():
            db_time = self.get_db_time_from_local_time(getattr(leg_entry, input_field), airport_city)
            setattr(departure_orm, orm_field, db_time)
        arrival_orm = Arrival()
        airport_orm = self.get_or_add_airport(leg_entry.final_airport)
        arrival_orm.airport = airport_orm
        arrival_orm.gate = leg_entry.final_gate
        arrival_orm.concourse = leg_entry.final_concourse
        arrival_orm.terminal = leg_entry.final_terminal
        arrival_orm.runway = leg_entry.landing_runway
        airport_city = airport_orm.city
        arrival_times = {"landing_time": "landing_time_FA",
                         "planned_landing_time": "landing_time_planned_FA",
                         "gate_arrival_time": "gate_arrival_time_FA",
                         "planned_gate_arrival_time": "gate_arrival_time_planned_FA"}
        for orm_field, input_field in arrival_times.items():
            local_time = getattr(leg_entry, input_field)
            if len(local_time) != 0:
                db_time = self.get_db_time_from_local_time(local_time, airport_city)
            else:
                db_time = ''
            setattr(arrival_orm, orm_field, db_time)
        self.session.add(departure_orm)
        self.session.add(arrival_orm)
        leg_orm.departure = departure_orm
        leg_orm.arrival = arrival_orm
        self.session.add(leg_orm)
        return leg_orm

    def get_route(self, route_entry: InputRouteEntry, trip_orm: Trip):
        query = self.session.query(Route).filter(Route.trip_id == trip_orm.id, Route.seq == route_entry.segment_seq)
        if query.count() == 0:
            return None
        else:
            return query.one()

    def add_route(self, route_entry: InputRouteEntry, trip_orm: Trip):
        route_orm = Route()
        route_orm.seq = route_entry.segment_seq
        route_orm.type = route_entry.segment_type
        route_orm.flight = self.get_or_add_flight(route_entry.flight)
        trip_orm.ticket_number = route_entry.e_ticket_num
        route_orm.cabin = route_entry.cabin
        route_orm.seat = route_entry.seat
        route_orm.fare_code = route_entry.fare_code
        route_orm.boarding_group = route_entry.boarding_group
        route_orm.plane = self.get_or_add_plane(route_entry.plane, route_entry.plane_model,
                                                route_orm.flight.airline_id)
        route_orm.distance_FA = route_entry.miles_from_FA
        route_orm.trip = trip_orm
        self.session.add(route_orm)
        for leg in route_entry.legs:
            self.add_leg(leg, route_orm)
        return route_orm

    def get_or_add_route(self, route_entry: InputRouteEntry, trip_orm: Trip):
        route_orm = self.get_route(route_entry, trip_orm)
        if route_orm is None:
            route_orm = self.add_route(route_entry, trip_orm)
        return route_orm

    def get_trip(self, trip_entry: InputTripEntry):
        """Note: legacy trips may not have confirmation number; future trips should have it
        """
        query = self.session.query(Trip).filter_by(confirmation_number=trip_entry.confirmation_num)
        if query.count() == 0:
            return None
        else:
            return query.one()

    def add_trip(self, trip_entry: InputTripEntry):
        trip_orm = Trip()
        trip_orm.confirmation_number = trip_entry.confirmation_num
        trip_orm.price = trip_entry.price
        self.session.add(trip_orm)
        return trip_orm

    def get_or_add_trip(self, trip_entry: InputTripEntry, is_commit):
        trip_orm = self.get_trip(trip_entry)
        if trip_orm is None:
            trip_orm = self.add_trip(trip_entry)
        done_segments, total_segments = 0, 0
        trip_done = True
        for segment in trip_entry.segments:
            if segment.status == 'Done':
                self.get_or_add_route(segment, trip_orm)
                done_segments += 1
            total_segments += 1
        if done_segments != total_segments:
            trip_done = False
        if is_commit:
            self.session.commit()
        return trip_orm, trip_done


get_db_ops = singleton(FlightDbOps)

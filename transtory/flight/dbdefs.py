"""
Flight database definitions
"""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, Text


FlightDbModel = declarative_base()


class PlaneModel(FlightDbModel):
    """Plane type table: Category
    """
    # TODO: build up plane_type table
    __tablename__ = "plane_models"
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    maker = Column(Text)


class Plane(FlightDbModel):
    """Plane table: Object
    Plane is identified as tail number. The tail number may occasionally change with time for the same plane. The
        complexity is to be taken care of when it actually happens for the database
    """
    # TODO: handle the situation of the same plane with different tail numbers at different time points
    #   This case should be handled when it happens
    __tablename__ = "planes"
    id = Column(Integer, primary_key=True)
    tail_number = Column(Text)
    msn = Column(Text)
    airline_id = Column(Integer, ForeignKey("airlines.id"))
    model_id = Column(Integer, ForeignKey("plane_models.id"))
    nickname = Column(Text)
    airline = relationship("Airline", backref="planes")
    model = relationship("PlaneModel", backref="planes")


class Airport(FlightDbModel):
    """Airport table: Object
    """
    __tablename__ = "airports"
    id = Column(Integer, primary_key=True)
    city = Column(Text)
    iata = Column(Text)
    icao = Column(Text)
    name = Column(Text)


class Airline(FlightDbModel):
    """Airline: Object
    """
    __tablename__ = "airlines"
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    iata = Column(Text)
    icao = Column(Text)
    callsign = Column(Text)


class Flight(FlightDbModel):
    """Flight table: Object
    Flight is identified by the airline, number, start/final airport. As long as the elements remains the same, it is
        identified as the same flight.
    """
    __tablename__ = "flights"
    id = Column(Integer, primary_key=True)
    number = Column(Text)
    airline_id = Column(Integer, ForeignKey("airlines.id"))
    airline = relationship("Airline", backref="flights")
    start_id = Column(Integer, ForeignKey("flight_starts.id"))
    final_id = Column(Integer, ForeignKey("flight_finals.id"))
    start = relationship("FlightStart", uselist=False, backref="flight")
    final = relationship("FlightFinal", uselist=False, backref="flight")


class FlightStart(FlightDbModel):
    """Flight start table: Action
    """
    __tablename__ = "flight_starts"
    id = Column(Integer, primary_key=True)
    flight_id_retired = Column(Integer)
    airport_id = Column(Integer, ForeignKey("airports.id"))
    airport = relationship("Airport", backref="as_starts")


class FlightFinal(FlightDbModel):
    """Flight final table: Action
    """
    __tablename__ = "flight_finals"
    id = Column(Integer, primary_key=True)
    flight_id_retired = Column(Integer)
    airport_id = Column(Integer, ForeignKey("airports.id"))
    airport = relationship("Airport", backref="as_finals")


class Trip(FlightDbModel):
    """Trip table: Event
    """
    __tablename__ = "trips"
    id = Column(Integer, primary_key=True)
    confirmation_number = Column(Text)
    ticket_number = Column(Text)
    price = Column(Text)


class Route(FlightDbModel):
    """Route table: Event
    """
    __tablename__ = "routes"
    id = Column(Integer, primary_key=True)
    trip_id = Column(Integer, ForeignKey("trips.id"))
    seq = Column(Integer)
    type = Column(Integer)
    plane_id = Column(Integer, ForeignKey("planes.id"))
    flight_id = Column(Integer, ForeignKey("flights.id"))
    cabin = Column(Text)
    seat = Column(Text)
    fare_code = Column(Text)
    boarding_group = Column(Text)
    distance_FA = Column(Text)
    # departure_id = Column(Integer, ForeignKey("departures.id"))
    # arrival_id = Column(Integer, ForeignKey("arrivals.id"))
    trip = relationship("Trip", backref="routes")
    flight = relationship("Flight", backref="routes")
    plane = relationship("Plane", backref="routes")


class Leg(FlightDbModel):
    """Leg table: Event
    """
    __tablename__ = "legs"
    id = Column(Integer, primary_key=True)
    route_id = Column(Integer, ForeignKey("routes.id"))
    seq = Column(Integer)
    type = Column(Text)
    departure_id = Column(Integer, ForeignKey("departures.id"))
    arrival_id = Column(Integer, ForeignKey("arrivals.id"))
    route = relationship("Route", backref="legs")


class Departure(FlightDbModel):
    """Departure table: Action
    """
    __tablename__ = "departures"
    id = Column(Integer, primary_key=True)
    route_id_retired = Column(Integer)
    airport_id = Column(Integer, ForeignKey("airports.id"))
    terminal = Column(Text)
    concourse = Column(Text)
    gate = Column(Text)
    pushback_time = Column(Text)
    planned_pushback_time = Column(Text)
    runway = Column(Text)
    takeoff_time = Column(Text)
    planned_takeoff_time = Column(Text)
    note = Column(Text)
    airport = relationship("Airport", backref="departures")
    leg = relationship("Leg", uselist=False, backref="departure")


class Arrival(FlightDbModel):
    """Arrival table: Action
    """
    __tablename__ = "arrivals"
    id = Column(Integer, primary_key=True)
    route_id_retired = Column(Integer)
    type = Column(Text)
    airport_id = Column(Integer, ForeignKey("airports.id"))
    runway = Column(Text)
    landing_time = Column(Text)
    planned_landing_time = Column(Text)
    terminal = Column(Text)
    concourse = Column(Text)
    gate = Column(Text)
    gate_arrival_time = Column(Text)
    planned_gate_arrival_time = Column(Text)
    note = Column(Text)
    airport = relationship("Airport", backref="arrivals")
    leg = relationship("Leg", uselist=False, backref="arrival")

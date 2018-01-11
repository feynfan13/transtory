"""
Flight database definitions
"""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, Text


FlightDbModel = declarative_base()


class PlaneType(FlightDbModel):
    """Plane type table: Category
    """
    __tablename__ = "plane_types"
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    maker = Column(Text)


class Plane(FlightDbModel):
    """Plane table: Object
    Plane is identified as tail number. The tail number may occasionally change with time for the same plane. The
        complexity is to be taken care of when it actually happens for the database
    """
    # TODO: handle the situation of the same plane with different tail numbers at different time points
    __tablename__ = "planes"
    id = Column(Integer, primary_key=True)
    tail_number = Column(Text)
    msn = Column(Text)
    airline_id = Column(Integer, ForeignKey("airlines.id"))
    # TODO: move the plane type to a separate table
    type = Column(Text)
    nickname = Column(Text)
    airline = relationship("Airline", backref="planes")


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
    __tablename__ = ""
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


class FlightStart(FlightDbModel):
    """Flight start table: Action
    """
    __tablename__ = "flight_starts"
    id = Column(Integer, primary_key=True)
    flight_id = Column(Integer, ForeignKey("flights.id"))
    airport_id = Column(Integer, ForeignKey("airports.id"))
    flight = relationship("Flight", uselist=False, backref="start")
    airport = relationship("Airport", backref="as_starts")


class FlightFinal(FlightDbModel):
    """Flight final table: Action
    """
    __tablename__ = "flight_finals"
    id = Column(Integer, primary_key=True)
    flight_id = Column(Integer, ForeignKey("flights.id"))
    airport_id = Column(Integer, ForeignKey("airports.id"))
    flight = relationship("Flight", uselist=False, backref="final")
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
    leg_type = Column(Integer)
    plane_id = Column(Integer, ForeignKey("planes.id"))
    flight_id = Column(Integer, ForeignKey("flights.id"))
    cabin = Column(Text)
    seat = Column(Text)
    fare_code = Column(Text)
    boarding_group = Column(Text)
    distance = Column(Text)
    plane = relationship("Plane", backref="routes")
    flight = relationship("Flight", backref="routes")


class Departure(FlightDbModel):
    """Departure table: Action
    """
    __tablename__ = "departures"
    id = Column(Integer, primary_key=True)
    route_id = Column(Integer, ForeignKey("routes.id"))
    type = Column(Text)
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
    route = relationship("Route", uselist=False, backref="departure")
    airport = relationship("Airport", backref="departures")


class Arrival(FlightDbModel):
    """Arrival table: Action
    """
    __tablename__ = "arrivals"
    id = Column(Integer, primary_key=True)
    route_id = Column(Integer, ForeignKey("routes.id"))
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
    route = relationship("Route", uselist=False, backref="arrival")
    airport = relationship("Airport", backref="arrivals")

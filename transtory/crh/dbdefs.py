"""
China Railway Highspeed (CRH) database definitions
"""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, Text, Float


CrhDbModel = declarative_base()


class TrainType(CrhDbModel):
    """Train type table: Category
    """
    __tablename__ = "train_types"
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    code = Column(Text)


class Train(CrhDbModel):
    """Train table: Object
    """
    __tablename__ = "trains"
    id = Column(Integer, primary_key=True)
    sn = Column(Text)
    note = Column(Text)
    type_id = Column(Integer, ForeignKey("train_types.id"))
    type = relationship("TrainType", backref="trains")


class Line(CrhDbModel):
    """Line table: Object
    Line are specified by line number, line origin, and line destination, as line with the same line number may have
        different origin and destination with time
    """
    __tablename__ = "lines"
    id = Column(Integer, primary_key=True)
    name = Column(Text)


class Station(CrhDbModel):
    """Station table: Object
    Stations are specified station name. WARNING: station name may occasionally change, which needs manual update
    """
    __tablename__ = "stations"
    id = Column(Integer, primary_key=True)
    chn_name = Column(Text)


class LineStart(CrhDbModel):
    """Line start table: Action
    """
    __tablename__ = "line_origins"
    id = Column(Integer, primary_key=True)
    line_id = Column(Integer, ForeignKey("lines.id"))
    station_id = Column(Integer, ForeignKey("stations.id"))
    line = relationship("Line", uselist=False, backref="line_origin")
    station = relationship("Station", backref="as_starts")


class LineFinal(CrhDbModel):
    """Line final table: Action
    """
    __tablename__ = "line_destinations"
    id = Column(Integer, primary_key=True)
    line_id = Column(Integer, ForeignKey("lines.id"))
    station_id = Column(Integer, ForeignKey("stations.id"))
    line = relationship("Line", uselist=False, backref="line_destination")
    station = relationship("Station", backref="as_finals")


class Task(CrhDbModel):
    """Task table: Object
    """
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True)
    content = Column(Text)


class Ticket(CrhDbModel):
    """Ticket table: Object
    Ticket means the paper you got from 12306.
    In some cases, some fields are lost, such as when using ID card or public transportation card
    """
    # TODO: at present ticket is mangled in trip table; we need to separate them out
    __tablename__ = "tickets"
    id = Column(Integer, primary_key=True)
    short_sn = Column(Text)
    long_sn = Column(Text)
    sold_by = Column(Text)
    sold_type = Column(Text)
    trip = relationship("Trip", uselist=False, backref="ticket")


class Trip(CrhDbModel):
    """Trip table: Event
    Trip means the transit specified by a railway ticket
    """
    # TODO: at present ticket is mangled in trip table; we need to separate them out
    __tablename__ = "trips"
    id = Column(Integer, primary_key=True)
    task_id = Column(Integer, ForeignKey("tasks.id"))
    line_id = Column(Integer, ForeignKey("lines.id"))
    task = relationship("Task", backref="trips")
    line = relationship("Line", backref="trips")
    seat_type = Column(Text)
    seat_number = Column(Text)
    price = Column(Text)
    ticket_number = Column(Text)
    ticket_sn = Column(Text)
    ticket_sold_by = Column(Text)
    ticket_sold_type = Column(Text)
    ticket_id = Column(Integer, ForeignKey("tickets.id"))
    note = Column(Text)


class Route(CrhDbModel):
    """Route table: Event
    Route means taking a train from one station to another.
    This layer is setup for the pattern of exchange within the same trip, such as getting of at Beijing for
        Shanghai-Changchun line. But this pattern is not seen up to now (2018-01-09)
    """
    __tablename__ = "routes"
    id = Column(Integer, primary_key=True)
    trip_id = Column(Integer, ForeignKey("trips.id"))
    carriage = Column(Text)
    note = Column(Text)
    trip = relationship("Trip", backref="routes")


class Departure(CrhDbModel):
    """Departure table: Action
    """
    __tablename__ = "departures"
    id = Column(Integer, primary_key=True)
    route_id = Column(Integer, ForeignKey("routes.id"))
    station_id = Column(Integer, ForeignKey("stations.id"))
    # TODO: merge date and time to a single time
    date = Column(Text)
    time = Column(Text)
    # TODO: change planned time to a datetime string
    planned_time = Column(Text)
    gate = Column(Text)
    platform = Column(Text)
    note = Column(Text)
    route = relationship("Route", uselist=False, backref="departure")
    station = relationship("Station", backref="departures")


class Arrival(CrhDbModel):
    """Arrival table: Action
    """
    __tablename__ = "arrivals"
    id = Column(Integer, primary_key=True)
    route_id = Column(Integer, ForeignKey("routes.id"))
    station_id = Column(Integer, ForeignKey("stations.id"))
    route = relationship("Route", uselist=False, backref="arrival")
    station = relationship("Station", backref="arrivals")


class TrainService(CrhDbModel):
    """Train service table: Action
    """
    __tablename__ = "train_services"
    id = Column(Integer, primary_key=True)
    route_id = Column(Integer, ForeignKey("routes.id"))
    train_id = Column(Integer, ForeignKey("trains.id"))
    # At present, operation type is designated by an integer
    #   -- 0: trainset of the seat
    #   -- 1: joined trainset
    #   -- 2: joined trainset at backward position (seat trainset at forward position)
    #   -- 3: joined trainset at forward position (seat trainset at backward position)
    # TODO: improve the logic; it is ugly now
    operation_type = Column(Integer)
    note = Column(Text)
    route = relationship("Route", uselist=False, backref="train_service")
    train = relationship("Train", backref="services")

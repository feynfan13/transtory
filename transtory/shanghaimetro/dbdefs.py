"""
Shanghai Metro database definitions
"""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, Text, Float


ShmDbModel = declarative_base()


# Section for lines
class Line(ShmDbModel):
    """Shanghai Metro lines
    """
    __tablename__ = "lines"
    id = Column(Integer, primary_key=True)
    name = Column(Text)

    def __repr__(self):
        # TODO
        pass


# Section for trains
class TrainType(ShmDbModel):
    """Train type table: Category
    """
    __tablename__ = "train_types"
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    maker = Column(Text)
    display_name = Column(Text)
    note = Column(Text)

    def __repr__(self):
        return "<Train type (name = {:s}, maker = {:s})>".format(self.name, self.maker)


class Train(ShmDbModel):
    """Train table: Object
    Train means a trainset with multiple  identified by a SN. Trainsets are rarely unlinked.
    Unlink/carriage reorganization may happen for special reasons/events, such as expanding from 6-carriage to
        8-carriage trains of line 01/02, replacing destroyed carriages of train 0117
    Each train are loosely bound to a line. But 03A02/04A02 are occasionally sharing their trains.
    """
    __tablename__ = "trains"
    id = Column(Integer, primary_key=True)
    sn = Column(Text)
    # Trains may not operate on its line, such as shared trains for line 3/4
    line_id = Column(Integer, ForeignKey("lines.id"))
    train_type_id = Column(Integer, ForeignKey("train_types.id"))
    line = relationship("Line", backref='trains')
    trian_type = relationship("TrainType", backref="trains")

    def __repr__(self):
        return "<Train (sn = {:s}, type = {:s})>".format(self.sn, self.train_type.name)


class Station(ShmDbModel):
    """Station table: Object
    Station means one station on one line.
    Stations with the same name are exchange stations.
    One exception is, 浦电路 on line 06 and line 04, which are not exchange stations
    """
    __tablename__ = "stations"
    id = Column(Integer, primary_key=True)
    sn = Column(Text)
    chn_name = Column(Text)
    eng_name = Column(Text)
    line_id = Column(Integer, ForeignKey("lines.id"))
    distance = Column(Text)
    line = relationship("Line", backref="stations")


class Task(ShmDbModel):
    """Task table: Category
    Task is a loose string describing the purpose of several routes
    """
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True)
    task = Column(Text)


class Departure(ShmDbModel):
    """Route departure table: Action
    Departure means leaving a station at a specific time
    """
    __tablename__ = "departures"
    id = Column(Integer, primary_key=True)
    route_id = Column(Integer, ForeignKey("routes.id"))
    station_id = Column(Integer, ForeignKey("stations.id"))
    time = Column(Text)
    date_retire = Column(Text)
    time_retire = Column(Text)
    route = relationship("Route", uselist=False, backref="departure")
    station = relationship("Station", backref="departures")


class Arrival(ShmDbModel):
    """Route arrival table: Action
    Arrival means reaching a station at a specific time
    """
    __tablename__ = "arrivals"
    id = Column(Integer, primary_key=True)
    route_id = Column(Integer, ForeignKey("routes.id"))
    station_id = Column(Integer, ForeignKey("stations.id"))
    time = Column(Text)
    time_retire = Column(Text)
    route = relationship("Route", uselist=False, backref="arrival")
    station = relationship("Station", backref="arrivals")


class Route(ShmDbModel):
    """Route table: Event
    Route means the event from one station to another by one trainset
    """
    __tablename__ = "routes"
    id = Column(Integer, primary_key=True)
    task_id = Column(Integer, ForeignKey("tasks.id"))
    seq_retire = Column(Integer)
    train_id = Column(Integer, ForeignKey("trains.id"))
    note = Column(Text)
    train = relationship("Train", backref="routes")
    task = relationship("Task", backref="routes")

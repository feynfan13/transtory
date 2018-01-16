"""
Mobike trip database definitions
"""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, Text, Float


MobikeDbModel = declarative_base()


# Section for bike
class BikeType(MobikeDbModel):
    """Mobike types: Categorical table
    Each bike type can have multiple subtypes.
    """
    __tablename__ = "bike_types"
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    codename = Column(Text)

    def __repr__(self):
        return "<Bike type (name = {:s})>".format(self.name)


class BikeSubtype(MobikeDbModel):
    """Mobike subtypes: Categorical table
    Subtype is used directly to express bike type.
    """
    __tablename__ = "bike_subtypes"
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    type_id = Column(Integer, ForeignKey('bike_types.id'))

    def __repr__(self):
        return "<Mobike subtype (name = {:s})>".format(self.name)


BikeSubtype.type = relationship("BikeType", back_populates="subtypes")
BikeType.subtypes = relationship("BikeSubtype", order_by=BikeSubtype.id, back_populates="type")


class Bike(MobikeDbModel):
    """Mobike bikes: Object table
    Each bike has a unique SN, and is associated with a subtype.
    """
    __tablename__ = "bikes"
    id = Column(Integer, primary_key=True)
    sn = Column(Text)
    # If bike subtype is unknown, use the default for bike type in bike subtypes table
    subtype_id = Column(Integer, ForeignKey('bike_subtypes.id'))
    subtype = relationship("BikeSubtype", backref="bikes")

    def __repr__(self):
        return "<Bike (SN = {:s}, Subtype = {:s})>".format(self.sn, self.subtype.name)


class Trip(MobikeDbModel):
    """Mobike trips: Event table
    Trip can be identified by the time column. Currently, time is stored as a ISO8601 string in UTC time zone.
        When query a string becomes efficiency bottleneck in the future, consider change time format to integer.
    """
    __tablename__ = "trips"
    id = Column(Integer, primary_key=True)
    bike_service_id = Column(Integer, ForeignKey('bike_services.id'))
    # TODO: move city to a table
    city = Column(Text)
    time = Column(Text)
    departure_region = Column(Text)
    departure_place = Column(Text)
    departure_coordinate = Column(Text)
    arrival_region = Column(Text)
    arrival_place = Column(Text)
    arrival_coordinate = Column(Text)
    duration = Column(Integer)
    distance = Column(Float)
    note = Column(Text)

    def __repr__(self):
        return "<Trip(time = {:s}, departure = {:s}, arrival = {:s})>".format(
            self.departure_time, self.departure_region, self.arrival_region)


class BikeService(MobikeDbModel):
    """Mobike bike services: Action
    A note can be attached to each service
    """
    __tablename__ = "bike_services"
    id = Column(Integer, primary_key=True)
    bike_id = Column(Integer, ForeignKey('bikes.id'))
    note = Column(Text)
    trip = relationship("Trip", uselist=False, backref='bike_service')
    bike = relationship("Bike", backref='services')

    def __repr__(self):
        return "<Bike service(bike sn = {:s}, trip time = {:s}>".format(
            self.bike.sn, self.trip.departure_time)

"""
Shanghai bus database definitions
"""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, Text, Float


ShbDbModel = declarative_base()


# Section for bus brand
class BusBrand(ShbDbModel):
    """Bus brand
    """
    __tablename__ = 'bus_brand'
    id = Column(Integer, primary_key=True)
    name = Column(Text)

    def __repr__(self):
        # TODO
        pass


# Section for bus type
class BusType(ShbDbModel):
    """Bus type: Category
    """
    __tablename__ = "bus_type"
    id = Column(Integer, primary_key=True)
    type = Column(Text)
    brand_id = Column(Text, ForeignKey("bus_brand.id"))
    brand = relationship("BusBrand", backref="bus_types")
    comment = Column(Text)

    def __repr__(self):
        # TODO
        pass

class Company(ShbDbModel):
    """Shanghai bus company
    """
    __tablename__ = "company"
    id = Column(Integer, primary_key=True)
    name = Column(Text)

    def __repr__(self):
        # TODO
        pass

class BusTypeCompany(ShbDbModel):
    """Company-level info of bus type
    """
    __tablename__ = "bus_type_company"
    id = Column(Integer, primary_key=True)
    bus_type_id = Column(Integer, ForeignKey("bus_type.id"))
    company_id = Column(Integer, ForeignKey("company.id"))
    bus_type = relationship("BusType", backref="companies")
    company = relationship("Company", backref="bus_types")
    model = Column(Text)
    online_time = Column(Text)

    def __repr__(self):
        return "<Train (sn = {:s}, type = {:s})>".format(self.sn, self.train_type.name)

from transtory.common import DatabaseOpsBase, singleton
from transtory.common import DateTimeHelper

from .configs import get_datetime_helper
from .configs import logger
from .configs import MobikeSysConfigs, get_configs

from .publicdata import MobikePublicData, get_public_data

from .dbdefs import MobikeDbModel, Bike, BikeType, BikeSubtype, Trip, BikeService


class MobikeDbOps(DatabaseOpsBase):
    """Operations of Mobike database, including
        -- data transformers: get trip id from date and time string
        -- empty database creation
        -- query operations:
        -- insertion operations:
    """
    def __init__(self):
        self.configs: MobikeSysConfigs = get_configs()
        self.public_data: MobikePublicData = get_public_data()
        self.dt_helper: DateTimeHelper = get_datetime_helper()
        super(MobikeDbOps, self).__init__(self.configs.db_path)
        logger.info("Created MobikeDbOps instance.")

    # Method type: create public data tables
    def update_bike_type_table(self):
        logger.info("Updating the mobike bike type table.")
        bike_types = self.public_data.get_bike_types()
        for bike_type in bike_types:
            query = self.session.query(BikeType).filter_by(name=bike_type[0])
            type_dict = {"name": bike_type[0], "codename": bike_type[1]}
            if query.count() == 0:
                type_orm = BikeType(**type_dict)
                self.session.add(type_orm)
            else:
                type_orm = query.one()
                self.update_dict_to_orm(type_orm, type_dict)
        self.session.commit()

    def update_bike_subtype_table(self):
        logger.info("Updating the mobike bike subtype table.")
        bike_subtypes = self.public_data.get_bike_subtypes()
        for bike_subtype in bike_subtypes:
            type_query = self.session.query(BikeType).filter_by(name=bike_subtype[1])
            subtype_dict = {"name": bike_subtype[0], "type_id": type_query.one().id}
            query = self.session.query(BikeSubtype).filter_by(name=bike_subtype[0])
            if query.count() == 0:
                subtype_orm = BikeSubtype(**subtype_dict)
                self.session.add(subtype_orm)
            else:
                subtype_orm = query.one()
                self.update_dict_to_orm(subtype_orm, subtype_dict)
        self.session.commit()

    def create_db_structure(self):
        """Create or validate database structure
        """
        logger.info("Creating mobike database structure.")
        MobikeDbModel.metadata.create_all(bind=self.engine)
        self.update_bike_type_table()
        self.update_bike_subtype_table()

    # Method type: transforming input data to database data
    def get_trip_id_from_date_time_str(self, date_str, time_str):
        date_int = self.dt_helper.get_date_int_from_date_str(date_str)
        time_int = self.dt_helper.get_time_int_from_time_str(time_str)
        return date_int * 24 * 60 + time_int

    def get_trip_id_from_date_time(self, date, time):
        date_int = self.dt_helper.get_date_int(date)
        time_int = self.dt_helper.get_time_int(time)
        return date_int * 24 * 60 + time_int

    # Method type: query, insert, or update objects or events
    def get_bike_subtype(self, subtype_name):
        return self.session.query(BikeSubtype).filter(BikeSubtype.name == subtype_name).one()

    def get_bike(self, bike_sn):
        query = self.session.query(Bike).filter(Bike.sn == bike_sn)
        return query.one() if query.count() != 0 else None

    def insert_bike(self, sn, subtype):
        subtype_orm = self.get_bike_subtype(subtype)
        bike_orm = Bike(sn=sn)
        bike_orm.subtype = subtype_orm
        self.session.add(bike_orm)
        # self.session.commit()
        return bike_orm

    def insert_bike_service(self, big_dict):
        bike_sn = big_dict["bike_sn"]
        bike_orm = self.get_bike(bike_sn)
        if bike_orm is None:
            bike_orm = self.insert_bike(bike_sn, big_dict["bike_subtype_name"])
        bike_service_orm = BikeService(note=big_dict["bike_service_note"], bike=bike_orm)
        self.session.add(bike_service_orm)
        # self.session.commit()
        return bike_service_orm

    def get_trip(self, trip_id):
        query = self.session.query(Trip).filter(Trip.id == trip_id)
        return query.one() if query.count() != 0 else None

    def insert_trip(self, big_dict):
        trip_dict = dict()
        trip_fields = ["city", "departure_time", "departure_region", "departure_place",
                       "departure_coordinate", "arrival_region", "arrival_place",
                       "arrival_coordinate", "trip_duration", "trip_distance", "trip_note"]
        for key in trip_fields:
            trip_dict[key] = big_dict[key]
        trip_dict["id"] = big_dict["trip_id"]
        trip_orm = Trip(**trip_dict)
        trip_orm.bike_service = self.insert_bike_service(big_dict)
        self.session.add(trip_orm)
        # self.session.commit()
        return trip_orm


get_mobike_db_ops = singleton(MobikeDbOps)

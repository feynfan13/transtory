from transtory.common import DatabaseOpsBase, singleton
from transtory.common import DateTimeHelper

from .configs import get_datetime_helper
from .configs import logger
from .configs import MobikeSysConfigs, get_configs

from .publicdata import MobikePublicData, get_public_data

from .dbdefs import MobikeDbModel, Bike, BikeType, BikeSubtype, Trip, BikeService


class BikeEntry(object):
    def __init__(self):
        self.sn = None
        self.subtype = None


class TripEntry(object):
    def __init__(self):
        self.city = None
        self.time = None
        self.departure_region = None
        self.departure_place = None
        self.departure_coordinate = None
        self.arrival_region = None
        self.arrival_place = None
        self.arrival_coordinate = None
        self.duration = None
        self.distance = None
        self.trip_note = None
        self.bike_sn = None
        self.bike_subtype = None
        self.bike_note = None

    def get_bike_entry(self):
        bike_entry = BikeEntry()
        bike_entry.sn, bike_entry.subtype = self.bike_sn, self.bike_subtype
        return bike_entry


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

    def get_db_time_from_entry_time(self, entry: TripEntry):
        eng_city = self.public_data.get_city_eng_name(entry.city)
        return self.dt_helper.get_datetime_str(self.dt_helper.get_utc_datetime(entry.time, eng_city))

    # Method type: query, insert, or update objects or events
    def get_bike_subtype(self, subtype_name):
        return self.session.query(BikeSubtype).filter(BikeSubtype.name == subtype_name).one()

    def get_bike(self, bike_sn):
        query = self.session.query(Bike).filter(Bike.sn == bike_sn)
        return query.one() if query.count() != 0 else None

    def add_bike(self, bike_entry: BikeEntry):
        """Add bike to database.
        WARNING: check if the bike is already present in the database before addition
        """
        subtype_orm = self.get_bike_subtype(bike_entry.subtype)
        bike_orm = Bike(sn=bike_entry.sn)
        bike_orm.subtype = subtype_orm
        self.session.add(bike_orm)
        self.session.commit()
        logger.info("Added bike {:s} of subtype {:s}".format(bike_entry.sn, bike_entry.subtype))
        return bike_orm

    def update_bike(self, bike_orm: Bike, bike_entry: BikeEntry):
        """Update bike info.
        Note bike sn is NOT updated here; new sn means new bike
        """
        assert(bike_orm.sn == bike_entry.sn)
        if bike_orm.subtype.name != bike_entry.subtype:
            logger.info("Update bike subtype: {:s} -> {:s}".format(bike_orm.subtype.name, bike_entry.subtype))
            bike_orm.subtype = self.get_bike_subtype(bike_entry.subtype)
            return True
        else:
            return False

    def get_trip(self, entry: TripEntry):
        """Get trip orm object from database
        If the trip does not exist, return None.
        """
        eng_city = self.public_data.get_city_eng_name(entry.city)
        utc_time = self.dt_helper.get_datetime_str(self.dt_helper.get_utc_datetime(entry.time, eng_city))
        query = self.session.query(Trip).filter_by(time=utc_time)
        if query.count() != 0:
            return query.one()
        else:
            return None

    def add_trip(self, entry:TripEntry):
        """Add trip to database
        WARNING: check if the trip exist in the database; the function do not take this responsibility for efficiency.
        """
        bike_orm = self.get_bike(entry.bike_sn)
        if bike_orm is None:
            bike_orm = self.add_bike(entry.get_bike_entry())
        else:
            assert(entry.bike_subtype == bike_orm.subtype.name)
            logger.note("Bike {:s} is already in the database.".format(entry.bike_sn))
        bike_service_orm = BikeService(bike=bike_orm, note=entry.bike_note)
        self.session.add(bike_service_orm)
        utc_time = self.get_db_time_from_entry_time(entry)
        trip_orm = Trip(city=entry.city, time=utc_time, departure_place=entry.departure_place,
                        departure_region=entry.departure_region, departure_coordinate=entry.departure_coordinate,
                        arrival_place=entry.arrival_place, arrival_region=entry.arrival_region,
                        arrival_coordinate=entry.arrival_coordinate, duration=entry.duration, distance=entry.distance,
                        note=entry.trip_note)
        trip_orm.bike_service = bike_service_orm
        self.session.add(trip_orm)
        self.session.commit()
        return trip_orm

    def update_trip(self, trip_orm: Trip, entry: TripEntry):
        """Passing trip_orm in to reduce one possible query.
        """
        trip_updated = False
        bike_entry, bike_orm = entry.get_bike_entry(), trip_orm.bike_service.bike
        if bike_entry.sn == bike_orm.sn:  # If the same bike
            trip_updated = trip_updated or self.update_bike(bike_orm, bike_entry)
        else:  # Bike sn is rarely updated, so this logic should rarely be touched
            bike_service_orm, old_bike_orm = trip_orm.bike_service, trip_orm.bike_service.bike
            bike_orm = self.add_bike(bike_entry)
            bike_service_orm.bike = bike_orm
            if len(old_bike_orm.services) == 0:  # remove old bike if orphaned
                logger.warning("Delete bike {:s} within trip update".format(old_bike_orm.sn))
                self.session.delete(old_bike_orm)
            trip_updated = True
        if trip_orm.bike_service.note != entry.bike_note:
            logger.info("Update bike service: {:s} -> {:s}".format(trip_orm.bike_service.note, entry.bike_note))
            trip_orm.bike_service.note = entry.bike_note
            trip_updated = True
        db_time = self.get_db_time_from_entry_time(entry)
        if trip_orm.time != db_time:
            logger.info("Update trip field time: {:s} -> {:s}".format(trip_orm.time, db_time))
            trip_orm.time = db_time
            trip_updated = True
        trip_fields = [("city", "city"), ("departure_place", "departure_place"),
                       ("departure_region", "departure_region"), ("departure_coordinate", "departure_coordinate"),
                       ("arrival_place", "arrival_place"), ("arrival_region", "arrival_region"),
                       ("arrival_coordinate", "arrival_coordinate"), ("duration", "duration"),
                       ("distance", "distance"), ("note", "trip_note")]
        for orm_field, entry_field in trip_fields:
            orm_val, entry_val = getattr(trip_orm, orm_field), getattr(entry, entry_field)
            if orm_val != entry_val:
                logger.info("Update trip field {:s}: {:s} -> {:s}".format(orm_field, orm_val, entry_val))
                setattr(trip_orm, orm_field, entry_val)
                trip_updated = True
        if trip_updated:
            self.session.commit()
        return trip_updated


get_mobike_db_ops = singleton(MobikeDbOps)

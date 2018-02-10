from pytz import timezone

from transtory.common import DatabaseOpsBase, singleton
from transtory.common import DateTimeHelper

from .configs import get_datetime_helper
from .configs import logger
from .configs import FlightSysConfigs, get_configs

from .publicdata import FlightPublicDataApp, get_public_data_app

from .dbdefs import FlightDbModel, Flight, Airline


class InputTripEntry(object):
    def __init__(self):
        pass


class FlightDbOps(DatabaseOpsBase):
    """Operations of CRH database, including
    """
    def __init__(self):
        self.configs: FlightSysConfigs = get_configs()
        self.data_app: FlightPublicDataApp = get_public_data_app()
        self.dt_helper: DateTimeHelper = get_datetime_helper()
        super(FlightDbOps, self).__init__(self.configs.db_path)
        logger.info("Created CrhDbOps instance.")

    def create_db_structure(self):
        """Create or validate database structure
        """
        logger.info("Creating flight database structure.")
        FlightDbModel.metadata.create_all(bind=self.engine)

    def get_flight_num(self, flight_orm: Flight):
        return flight_orm.airline.iata + " " + flight_orm.number

    def get_local_time_from_db_time(self, atime_str, city):
        atz = self.dt_helper.get_time_zone_of_city(city)
        adt = self.dt_helper.get_datetime_from_str(atime_str)
        adt = adt.replace(tzinfo=timezone("UTC"))
        return self.dt_helper.get_datetime_str(adt.astimezone(atz))


get_db_ops = singleton(FlightDbOps)

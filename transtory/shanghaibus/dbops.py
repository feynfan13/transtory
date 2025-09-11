from transtory.common import DatabaseOpsBase, singleton
from transtory.common import DateTimeHelper

from .configs import get_datetime_helper
from .configs import logger
from .configs import ShbSysConfigs, get_configs

from .dbdefs import ShbDbModel
from .dbdefs import BusBrand, BusType, Company
from .dbdefs import BusTypeCompany


class ShbDbOps(DatabaseOpsBase):
    """Operations of Shanghai bus database, including
    """
    def __init__(self):
        self.configs: ShbSysConfigs = get_configs()
        self.dt_helper: DateTimeHelper = get_datetime_helper()
        super(ShbDbOps, self).__init__(self.configs.db_path)
        logger.info("Created CrhDbOps instance.")

    def create_db_structure(self):
        """Create or validate database structure
        """
        logger.info("Creating CRH database structure.")
        ShbDbModel.metadata.create_all(bind=self.engine)


get_db_ops = singleton(ShbDbOps)

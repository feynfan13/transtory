from transtory.common import DatabaseOpsBase, singleton
from transtory.common import DateTimeHelper

from .configs import get_datetime_helper
from .configs import logger
from .configs import CrhSysConfigs, get_configs

from .publicdata import CrhPublicDataApp, get_public_data_app
from .dbdefs import CrhDbModel


class InputTripEntry(object):
    def __init__(self):
        pass


class CrhDbOps(DatabaseOpsBase):
    """Operations of CRH database, including
    """
    def __init__(self):
        self.configs: CrhSysConfigs = get_configs()
        self.data_app: CrhPublicDataApp = get_public_data_app()
        self.dt_helper: DateTimeHelper = get_datetime_helper()
        super(CrhDbOps, self).__init__(self.configs.db_path)
        logger.info("Created CrhDbOps instance.")

    def create_db_structure(self):
        """Create or validate database structure
        """
        logger.info("Creating mobike database structure.")
        CrhDbModel.metadata.create_all(bind=self.engine)


get_db_ops = singleton(CrhDbOps)

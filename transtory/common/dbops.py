import os
import shutil
from .logging import transtory_logger
from datetime import datetime
import sqlalchemy
import sqlalchemy.orm


class DatabaseOpsBase(object):
    """Common database ops.
    """
    def __init__(self, db_path, test=False):
        self.engine, self.session_maker, self.session = None, None, None
        self.db_path = db_path
        if os.path.exists(self.db_path):
            transtory_logger.info("Use existing database.")
        else:
            transtory_logger.info("Create new database.")
        self.connect_db(test)
        self.backup_database()

    def connect_db(self, test):
        if self.engine is None:
            sqlalchemy.orm.configure_mappers()
            self.engine = sqlalchemy.create_engine("sqlite:///" + self.db_path, echo=test)
            self.session_maker = sqlalchemy.orm.sessionmaker(bind=self.engine)
            self.session = self.session_maker()

    def backup_database(self):
        time_stamp_str = datetime.now().strftime("%Y%m%d%H%M%S")
        backup_db_name = self.db_path+"_"+time_stamp_str+".bckp"
        shutil.copy(self.db_path, backup_db_name)

    @staticmethod
    def update_dict_to_orm(orm_object, record: dict):
        for key, val in record.items():
            db_val = getattr(orm_object, key)
            if db_val != val:
                setattr(orm_object, key, val)

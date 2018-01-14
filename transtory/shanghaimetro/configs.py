import os
import transtory.common as helpers


fs_helper = helpers.FileSystemHelper()


class ShmSysConfigs(object):
    def __init__(self):
        self.module_name = None
        self.root_folder = None
        self.db_name = None
        self.db_path = None
        self.trip_xlsx_name = None
        self.trip_xlsx_path = None
        self.stats_folder = None
        self.date_zero = None
        self.test_mode = None
        self.define_configs()

    def define_configs(self):
        self.module_name = "shanghaimetro"
        self.root_folder = fs_helper.get_parent_folder(os.path.abspath(__file__), 2)
        self.db_name = "ShanghaiMetroTrips.sqlite"
        self.db_path = os.sep.join([self.root_folder, "database", self.module_name, self.db_name])
        self.trip_xlsx_name = "ShanghaiMetroLog.xlsx"
        self.trip_xlsx_path = os.sep.join([self.root_folder, "log", self.module_name, self.trip_xlsx_name])
        self.stats_folder = os.sep.join([self.root_folder, "report", self.module_name])
        # TODO: change trip index to datetime integer format
        # self.date_zero = "2017-03-04"  # !!!DO NOT CHANGE!!!
        self.test_mode = False

    def switch_to_test_configs(self):
        self.db_name = "ShanghaiMetroTrips.sqlite"
        test_folder = os.sep.join([self.root_folder, "test"])
        self.db_path = os.sep.join([test_folder, "database", self.module_name, self.db_name])
        self.trip_xlsx_name = "ShanghaiMetroLog.xlsx"
        self.trip_xlsx_path = os.sep.join([test_folder, "log", self.module_name, self.trip_xlsx_name])
        self.stats_folder = os.sep.join([test_folder, "report", self.module_name])
        # TODO: change trip index to datetime integer format
        # self.date_zero = "2017-03-04"  # !!!DO NOT CHANGE!!!
        self.test_mode = True


get_configs = helpers.singleton(ShmSysConfigs)


def switch_to_test_mode():
    configs: ShmSysConfigs = get_configs()
    configs.switch_to_test_configs()


get_datetime_helper = helpers.singleton(helpers.DateTimeHelper, [get_configs().date_zero])

logger = helpers.transtory_logger.getChild("mobike")

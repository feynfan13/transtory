import os
import transtory.common as helpers


fs_helper = helpers.FileSystemHelper()


class ShmSysConfigs(helpers.ModuleSysConfigs):
    def __init__(self):
        super().__init__()
        self.module_name = None
        self.root_folder = None
        self.db_name = None
        self.db_path = None
        self.trip_xlsx_name = None
        self.trip_xlsx_path = None
        self.stats_folder = None
        self.publicdata_folder = None
        self.city = None
        self.test_mode = None
        self.date_zero = None
        self.define_configs()

    def define_configs(self):
        self.module_name = "shanghaimetro"
        self.root_folder = fs_helper.get_parent_folder(os.path.abspath(__file__), 2)
        self.db_name = "ShanghaiMetroTrips.sqlite"
        self.db_path = os.sep.join([self.data_folder, "database", self.module_name, self.db_name])
        self.trip_xlsx_name = "ShanghaiMetroLog.xlsx"
        self.trip_xlsx_path = os.sep.join([self.data_folder, "log", self.module_name, self.trip_xlsx_name])
        self.stats_folder = os.sep.join([self.result_folder, self.module_name])
        self.publicdata_folder = os.sep.join([self.data_folder, 'publicdata', self.module_name])
        self.city = "Shanghai"
        self.date_zero = "2013-07-01"
        self.test_mode = False

    def switch_to_test_configs(self):
        super().switch_to_test_configs()
        self.db_name = "ShanghaiMetroTrips.sqlite"
        test_folder = os.sep.join([self.root_folder, "test"])
        self.db_path = os.sep.join([test_folder, "database", self.module_name, self.db_name])
        self.trip_xlsx_name = "ShanghaiMetroLog.xlsx"
        self.trip_xlsx_path = os.sep.join([test_folder, "log", self.module_name, self.trip_xlsx_name])
        self.stats_folder = os.sep.join([test_folder, "report", self.module_name])
        self.test_mode = True


get_configs = helpers.singleton(ShmSysConfigs)


def switch_to_test_mode():
    configs: ShmSysConfigs = get_configs()
    configs.switch_to_test_configs()


get_datetime_helper = helpers.singleton(helpers.DateTimeHelper, [get_configs().date_zero])

logger = helpers.transtory_logger.getChild("mobike")

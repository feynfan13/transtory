import os
import transtory.common as helpers


fs_helper = helpers.FileSystemHelper()


class MobikeSysConfigs(object):
    """For mobike database
    date_zero: as Mobike has become international, date_zero is in UTC+00 time zone
    """
    def __init__(self):
        self.module_name = None
        self.root_folder = None
        self.db_name = None
        self.db_path = None
        self.trip_xlsx_name = None
        self.trip_xlsx_path = None
        self.stats_folder = None
        self.date_zero = None
        self.define_configs()

    def define_configs(self):
        self.module_name = "mobike"
        self.root_folder = fs_helper.get_parent_folder(os.path.abspath(__file__), 2)
        self.db_name = "MobikeTrips.sqlite"
        self.db_path = os.sep.join([self.root_folder, "database", self.module_name, self.db_name])
        self.trip_xlsx_name = "MobikeLogs.xlsx"
        self.trip_xlsx_path = os.sep.join([self.root_folder, "log", self.module_name, self.trip_xlsx_name])
        self.stats_folder = os.sep.join([self.root_folder, "report", self.module_name])
        self.date_zero = "2017-03-04"  # !!!DO NOT CHANGE!!!

    def switch_to_test_configs(self):
        self.db_name = "MobikeTrips.sqlite"
        test_folder = os.sep.join([self.root_folder, "test"])
        self.db_path = os.sep.join([test_folder, "database", self.module_name, self.db_name])
        self.trip_xlsx_name = "MobikeLogs.xlsx"
        self.trip_xlsx_path = os.sep.join([test_folder, "log", self.module_name, self.trip_xlsx_name])
        self.stats_folder = os.sep.join([test_folder, "report", self.module_name])
        # TODO: change trip index to datetime integer format
        self.date_zero = "2017-03-04"  # !!!DO NOT CHANGE!!!


# class MobikeTestSysConfigs(MobikeSysConfigs):
#     def __init__(self):
#         super(MobikeTestSysConfigs, self).__init__()
#         self.module_name = "mobike"
#         self.root_folder = fs_helper.get_parent_folder(os.path.abspath(__file__), 2)
#         self.db_name = "MobikeTripTest.sqlite"
#         self.db_path = os.sep.join([self.root_folder, "database", self.module_name, self.db_name])
#         self.trip_xlsx_name = "MobikeTest.xlsx"
#         self.trip_xlsx_path = os.sep.join([self.root_folder, "log", self.module_name, self.trip_xlsx_name])
#         self.date_zero = "2017-03-04"  # !!!DO NOT CHANGE!!!


get_configs = helpers.singleton(MobikeSysConfigs)


def switch_to_test_mode():
    configs: MobikeSysConfigs = get_configs()
    configs.switch_to_test_configs()


get_datetime_helper = helpers.singleton(helpers.DateTimeHelper, [get_configs().date_zero])
logger = helpers.transtory_logger.getChild("mobike")

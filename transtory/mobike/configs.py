import os
import transtory.common as helpers


fs_helper = helpers.FileSystemHelper()


class MobikeSysConfigs(object):
    def __init__(self):
        self.module_name = "mobike"
        self.root_folder = fs_helper.get_parent_folder(os.path.abspath(__file__), 2)
        self.db_name = "MobikeTrip.sqlite"
        self.db_path = os.sep.join([self.root_folder, "database", self.module_name, self.db_name])
        self.trip_xlsx_name = "Mobike.xlsx"
        self.trip_xlsx_path = os.sep.join([self.root_folder, "log", self.module_name, self.trip_xlsx_name])
        self.stats_folder = os.sep.join([self.root_folder, "report", self.module_name])
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
get_datetime_helper = helpers.singleton(helpers.DateTimeHelper, [get_configs().date_zero])
logger = helpers.transtory_logger.getChild("mobike")

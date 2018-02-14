import os
import transtory.common as helpers


fs_helper = helpers.FileSystemHelper()


class CrhSysConfigs(helpers.ModuleSysConfigs):
    def __init__(self):
        super().__init__()
        self.module_name = None
        self.root_folder = None
        self.db_name = None
        self.db_path = None
        self.log_folder = None
        self.log_archive_folder = None
        self.stats_folder = None
        self.test_mode = None
        self.date_zero = None
        self.define_configs()

    def define_configs(self):
        self.module_name = "crh"
        self.root_folder = fs_helper.get_parent_folder(os.path.abspath(__file__), 2)
        self.db_name = "CrhTransits.sqlite"
        self.db_path = os.sep.join([self.data_folder, "database", self.module_name, self.db_name])
        self.log_folder = os.sep.join([self.data_folder, "log", self.module_name])
        self.log_archive_folder = os.sep.join([self.log_folder, "logarchive"])
        self.stats_folder = os.sep.join([self.result_folder, self.module_name])
        self.date_zero = "2010-07-29"
        self.test_mode = False

    def switch_to_test_configs(self):
        super().switch_to_test_configs()
        test_folder = os.sep.join([self.root_folder, "test"])
        self.db_path = os.sep.join([test_folder, "database", self.module_name, self.db_name])
        self.log_folder = os.sep.join([self.root_folder, "log", self.module_name])
        self.log_archive_folder = os.sep.join([self.log_folder, "logarchive"])
        self.stats_folder = os.sep.join([test_folder, "report", self.module_name])
        self.test_mode = True


get_configs = helpers.singleton(CrhSysConfigs)


def switch_to_test_mode():
    configs: CrhSysConfigs = get_configs()
    configs.switch_to_test_configs()


get_datetime_helper = helpers.singleton(helpers.DateTimeHelper, [get_configs().date_zero])
logger = helpers.transtory_logger.getChild("crh")

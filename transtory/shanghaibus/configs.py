import os
import transtory.common as helpers


fs_helper = helpers.FileSystemHelper()


class ShbSysConfigs(helpers.ModuleSysConfigs):
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
        self.module_name = "shanghaibus"
        self.root_folder = fs_helper.get_parent_folder(os.path.abspath(__file__), 2)
        self.test_mode = False
        self.db_name = "ShanghaiBus.db"
        self.db_path = os.sep.join([self.data_folder, "database", self.module_name, self.db_name])
        self.stats_folder = os.sep.join([self.result_folder, self.module_name])
        self.city = "Shanghai"
        self.date_zero = "2013-07-01"


get_configs = helpers.singleton(ShbSysConfigs)


def switch_to_test_mode():
    configs: ShbSysConfigs = get_configs()
    configs.switch_to_test_configs()


get_datetime_helper = helpers.singleton(helpers.DateTimeHelper, [get_configs().date_zero])

logger = helpers.transtory_logger.getChild("shanghaibus")

from .configs import CrhSysConfigs, get_configs
from .dbops import CrhDbOps, get_db_ops


class CrhTrainStats(object):
    def __init__(self):
        self.configs: CrhSysConfigs = get_configs()
        self.save_folder = self.configs.stats_folder
        self.dbops: CrhDbOps = get_db_ops()
        self.session = self.dbops.session

    def _save_train_list(self):
        pass

    def save_all_stats(self):
        self._save_train_list()

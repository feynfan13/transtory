import os
import time

from .configs import FlightSysConfigs, get_configs
from .configs import logger

# from .dbdefs import Task, Trip, Route, Departure, Arrival, Station, Line
# from .dbdefs import Train, TrainService, TrainType

from .dbops import FlightDbOps, get_db_ops


class FlightTripStats(object):
    def __init__(self):
        pass
        self.configs: FlightSysConfigs = get_configs()
        self.save_folder = self.configs.stats_folder
        # self.dbops: FlightDbOps = get_db_ops()
        # self.session = self.dbops.session
        # self.route_fields = ["task", "train_number", "from", "from_time", "to", "to_time", "trainset", "note"]

    def _get_stats_full_path(self, fname):
        return os.path.sep.join([self.save_folder, fname])

    @staticmethod
    def _write_lists_to_csv(fout, val_list):
        """Goal of the function is to handle the None values properly
        """
        for val in val_list:
            if val is None:
                fout.write("||\t")
            elif isinstance(val, int):
                fout.write("|{:d}|\t".format(val))
            elif isinstance(val, str):
                fout.write("|{:s}|\t".format(val))
            else:
                raise Exception("Unsupported data type in csv writer.")

    def save_plane_list_csv(self):
        pass

    def save_all_stats(self):
        self.save_plane_list_csv()

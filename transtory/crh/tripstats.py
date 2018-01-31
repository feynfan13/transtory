import os
import time

from .configs import CrhSysConfigs, get_configs
from .configs import logger

from .dbdefs import Task, Trip, Route, Departure, Arrival, Station, Line
from .dbdefs import Train, TrainService, TrainType

from .dbops import CrhDbOps, get_db_ops


class CrhTripStats(object):
    def __init__(self):
        self.configs: CrhSysConfigs = get_configs()
        self.save_folder = self.configs.stats_folder
        self.dbops: CrhDbOps = get_db_ops()
        self.session = self.dbops.session
        self.route_fields = ["task", "train_number", "from", "from_time", "to", "to_time", "trainset", "note"]

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

    def _yield_route_list_entries(self):
        query = self.session.query(Task, Trip, Route).join(Task.trips).join(Trip.routes)
        for task, trip, route in query.all():
            results = list()
            results.append(task.content)
            # TODO: we should consider adding a null object for each object table, including line
            if trip.line is not None:
                results.append(trip.line.name)
            else:
                results.append("")
            results.append(route.departure.station.chn_name)
            results.append(route.departure.time)
            results.append(route.arrival.station.chn_name)
            results.append(route.arrival.time)
            # Train service
            train_services = route.train_services
            if len(train_services) == 0:
                trainset_str = ""
            elif len(train_services) == 1:
                train_service = train_services[0]
                trainset_str = train_service.train.sn
            elif len(train_services) == 2:
                ts0, ts1 = train_services
                if ts1.operation_type == 0:
                    ts0, ts1 = ts1, ts0
                if ts1.operation_type == 1:
                    trainset_str = "{:s} & [J]{:s}".format(ts0.train.sn, ts1.train.sn)
                elif ts1.operation_type == 2:
                    trainset_str = "[J]{:s} & {:s}->".format(ts1.train.sn, ts0.train.sn)
                elif ts1.operation_type == 3:
                    trainset_str = "{:s} & [J]{:s}->".format(ts0.train.sn, ts1.train.sn)
                else:
                    raise Exception("Invalid train service operation type.")
            else:
                raise Exception("More than 2 train service entry for one route.")
            results.append(trainset_str)
            results.append(route.note)
            yield results

    def save_route_list_csv(self):
        logger.info("Begin saving all routes.")
        start_time = time.clock()
        with open(self._get_stats_full_path("routes.csv"), "w", encoding="utf16") as fout:
            [fout.write("|{:s}|\t".format(x)) for x in self.route_fields]
            fout.write("\n")
            for result in self._yield_route_list_entries():
                self._write_lists_to_csv(fout, result)
                fout.write("\n")
        logger.info("Finished saving all routes (time used is {:f}s)".format(time.clock()-start_time))

    def save_all_stats(self):
        self.save_route_list_csv()

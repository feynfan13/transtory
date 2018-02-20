import os
import time
from sqlalchemy import func

from .configs import CrhSysConfigs, get_configs
from .configs import logger

from .dbdefs import Train, TrainType, TrainService
from .dbdefs import Station, Line, LineStart

from .dbops import CrhDbOps, get_db_ops


class CrhElementStats(object):
    def __init__(self):
        self.configs: CrhSysConfigs = get_configs()
        self.save_folder = self.configs.stats_folder
        self.dbops: CrhDbOps = get_db_ops()
        self.session = self.dbops.session
        self.train_fields = ["model", "train", "seat_count", "join_count"]
        self.line_fields = ["train_number", "from", "to"]

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

    def _yield_train_list_entries(self):
        # Seat trains
        query = self.session.query(TrainService.train_id, func.count('*').label("count"))
        stmt = query.filter(TrainService.operation_type == 0).group_by(TrainService.train_id).subquery()
        query = self.session.query(Train, stmt.c.count, TrainType).outerjoin(stmt, Train.id==stmt.c.train_id)
        query_seat = query.join(Train.type).order_by(Train.sn)
        # Join trains
        query_join = self.session.query(TrainService.train_id, func.count('*').label("count"))
        stmt_join = query_join.filter(TrainService.operation_type != 0).group_by(TrainService.train_id).subquery()
        query_join = self.session.query(Train, stmt_join.c.count).outerjoin(stmt_join, Train.id==stmt_join.c.train_id)
        query_join = query_join.order_by(Train.sn)
        for seat_trains, join_trains in zip(query_seat.all(), query_join.all()):
            train, seat_count, model = seat_trains
            join_count = join_trains[1]
            results = list()
            results.append(model.name)
            results.append(train.sn)
            results.append(seat_count)
            results.append(join_count)
            yield results

    def save_train_list_csv(self):
        logger.info("Begin saving all trains.")
        start_time = time.clock()
        with open(self._get_stats_full_path("trains.csv"), "w", encoding="utf16") as fout:
            [fout.write("|{:s}|\t".format(x)) for x in self.train_fields]
            fout.write("\n")
            for result in self._yield_train_list_entries():
                self._write_lists_to_csv(fout, result)
                fout.write("\n")
        logger.info("Finished saving all trains (time used is {:f}s)".format(time.clock() - start_time))

    def _yield_line_list_entries(self):
        query = self.session.query(Line, LineStart, Station).join(Line.start).join(LineStart.station)
        query = query.order_by(Station.chn_name)
        for line, _, station in query.all():
            results = list()
            results.append(line.name)
            results.append(station.chn_name)
            results.append(line.final.station.chn_name)
            yield results

    def save_line_list_csv(self):
        logger.info("Begin saving all lines.")
        start_time = time.clock()
        with open(self._get_stats_full_path("lines.csv"), "w", encoding="utf16") as fout:
            [fout.write("|{:s}|\t".format(x)) for x in self.line_fields]
            fout.write("\n")
            for result in self._yield_line_list_entries():
                self._write_lists_to_csv(fout, result)
                fout.write("\n")
        logger.info("Finished saving all lines (time used is {:f}s)".format(time.clock() - start_time))

    def save_all_stats(self):
        self.save_train_list_csv()
        self.save_line_list_csv()

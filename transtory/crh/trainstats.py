import os
import time
import re
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
        # Dependency: if train_fileds is changed, do changes to
        #   -- _get_train_list_sorter()
        #   -- _yield_train_list_entries()
        self.train_fields = ['seq', "model", "train", "seat_count", "join_count"]
        # Dependency: similar to train_fields
        self.line_fields = ['seq', 'train_number', 'from', 'to']

    def _get_stats_full_path(self, fname):
        return os.path.sep.join([self.save_folder, fname])

    @staticmethod
    def _write_lists_to_csv(fout, val_list):
        """Goal of the function is to handle the None values properly
        """
        for val in val_list:
            if val is None:
                fout.write("||,")
            elif isinstance(val, int):
                fout.write("{:d},".format(val))
            elif isinstance(val, str):
                fout.write("|{:s}|,".format(val))
            else:
                raise Exception("Unsupported data type in csv writer.")

    @staticmethod
    def _get_train_list_sorter(result):
        train_sn = result[1]
        train_seq = train_sn[-4:]
        if train_sn.startswith("CRH"):
            train_seg = "0"
        elif train_sn.startswith("CR"):
            train_seg = "1"
        else:
            raise ValueError("Invalid train sn ({:s}) in CRH module.".format(train_sn))
        return int(train_seg + train_seq)

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
        results_sorted = list()
        for seat_trains, join_trains in zip(query_seat.all(), query_join.all()):
            train, seat_count, model = seat_trains
            join_count = join_trains[1]
            seat_count = 0 if seat_count is None else seat_count
            join_count = 0 if join_count is None else join_count
            results = list()
            results.append(model.name)
            results.append(train.sn)
            results.append(seat_count)
            results.append(join_count)
            sort_val = self._get_train_list_sorter(results)
            results_sorted.append((sort_val, results))
        results_sorted.sort(key=lambda pair: pair[0])
        for _, results in results_sorted:
            yield results

    def save_train_list_csv(self):
        logger.info("Begin saving all trains.")
        start_time = time.clock()
        with open(self._get_stats_full_path("trains.csv"), "w", encoding="utf8") as fout:
            fout.write('\ufeff')
            [fout.write('{:s},'.format(x)) for x in self.train_fields]
            fout.write("\n")
            for idx, result in enumerate(self._yield_train_list_entries()):
                fout.write('{:d},'.format(idx+1))
                self._write_lists_to_csv(fout, result)
                fout.write("\n")
        logger.info("Finished saving all trains (time used is {:f}s)".format(time.clock() - start_time))

    @staticmethod
    def _get_line_list_sorter(result):
        train_number = result[0]
        seq = min([int(x) for x in re.findall(r'\d+', train_number)])
        seg_code = train_number[0]
        if seg_code == "D":
            seg_base = 00000
        elif seg_code == "G":
            seg_base = 10000
        elif seg_code == "C":
            seg_base = 20000
        else:
            raise ValueError("Invalid train number ({:s}) in CRH module".format(train_number))
        return seg_base + seq

    def _yield_line_list_entries(self):
        query = self.session.query(Line, LineStart, Station).join(Line.start).join(LineStart.station)
        query = query.order_by(Line.id)
        results_sorted = list()
        for line, _, station in query.all():
            results = list()
            results.append(line.name)
            results.append(station.chn_name)
            results.append(line.final.station.chn_name)
            sort_val = self._get_line_list_sorter(results)
            results_sorted.append((sort_val, results))
        results_sorted.sort(key=lambda pair: pair[0])
        for _, results in results_sorted:
            yield results

    def save_line_list_csv(self):
        logger.info("Begin saving all lines.")
        start_time = time.clock()
        with open(self._get_stats_full_path("lines.csv"), "w", encoding="utf8") as fout:
            fout.write('\ufeff')
            [fout.write("{:s},".format(x)) for x in self.line_fields]
            fout.write("\n")
            for idx, result in enumerate(self._yield_line_list_entries()):
                fout.write('{:d},'.format(idx+1))
                self._write_lists_to_csv(fout, result)
                fout.write("\n")
        logger.info("Finished saving all lines (time used is {:f}s)".format(time.clock() - start_time))

    def save_all_stats(self):
        self.save_train_list_csv()
        self.save_line_list_csv()

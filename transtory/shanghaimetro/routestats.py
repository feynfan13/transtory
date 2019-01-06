import os
import time
import pandas as pd

from .configs import logger

from .dbdefs import Train, Line, Station
from .dbdefs import Task, Route, Departure, Arrival
from .dbops import ShmDbOps, get_shm_db_ops
from .dbops import ShmSysConfigs, get_configs
from .dbops import DateTimeHelper, get_datetime_helper


class ShmTripStats(object):
    def __init__(self):
        self.configs = get_configs()
        self.save_folder = self.configs.stats_folder
        self.dbops: ShmDbOps = get_shm_db_ops()
        self.session = self.dbops.session

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
                raise Exception('Unsupported data type in csv writer.')

    def _def_route_list_query(self):
        columns = ['seq', 'task', 'line', 'train', 'from', 'from_time', 'to', 'to_time', 'note']
        query_dp = self.session.query(Route.id, Station.chn_name.label("start"),
                                      Departure.time.label("start_time"), Line.name.label("line"))
        stmt_dp = query_dp.join(Route.departure).join(Departure.station).join(Station.line).subquery()
        query_av = self.session.query(Route.id, Station.chn_name.label("end"), Arrival.time.label("end_time"))
        stmt_av = query_av.join(Route.arrival).join(Arrival.station).subquery()
        query = self.session.query(Task.task, stmt_dp.c.line, Train.sn, stmt_dp.c.start,
                                   stmt_dp.c.start_time, stmt_av.c.end, stmt_av.c.end_time, Route.note)
        query = query.join(Task.routes).join(Route.train, isouter=True).join(stmt_dp, Route.id == stmt_dp.c.id)
        query = query.join(stmt_av, Route.id == stmt_av.c.id)
        return columns, query

    def save_route_list_csv(self):
        logger.info("Begin saving all routes.")
        start_time = time.clock()
        columns, query = self._def_route_list_query()
        with open(self._get_stats_full_path("routes.csv"), "w", encoding="utf8") as fout:
            fout.write('\ufeff')
            [fout.write('{:s},'.format(x)) for x in columns]
            fout.write('\n')
            from_time_index, to_time_index = columns.index('from_time'), columns.index('to_time')
            for idx, route in enumerate(query.all()):
                result = [idx + 1]
                result += [val for val in route]
                result[from_time_index] = self.dbops.get_local_time_from_db_time([result[from_time_index]])[0]
                result[to_time_index] = self.dbops.get_local_time_from_db_time([result[to_time_index]])[0]
                self._write_lists_to_csv(fout, result)
                fout.write('\n')
        logger.info("Finished saving all routes (time used is {:f}s)".format(time.clock()-start_time))

    def save_route_list_html(self):
        pass

    def save_all_stats(self):
        self.save_route_list_csv()

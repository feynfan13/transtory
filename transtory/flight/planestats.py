import os
import time

from sqlalchemy import func

from .configs import FlightSysConfigs, get_configs
from .configs import logger

from .dbdefs import Plane, Airline, PlaneModel, Route

from .dbops import FlightDbOps, get_db_ops


class FlightPlaneStats(object):
    def __init__(self):
        self.configs: FlightSysConfigs = get_configs()
        self.save_folder = self.configs.stats_folder
        self.dbops: FlightDbOps = get_db_ops()
        self.session = self.dbops.session
        self.plane_fields = ["model", "airline", "tail_number", "route_count"]

    def _get_stats_full_path(self, fname):
        return os.path.sep.join([self.save_folder, fname])

    @staticmethod
    def _write_lists_to_csv(fout, val_list):
        """Goal of the function is to handle the None values properly
        """
        for val, mode in val_list:
            if mode:
                astr = '|'
            else:
                astr = ''
            if val is None:
                pass
            elif isinstance(val, int):
                astr += '{:d}'.format(val)
            elif isinstance(val, str):
                astr += '{:s}'.format(val)
            else:
                raise Exception("Unsupported data type in csv writer.")
            if mode:
                astr += '|,'
            else:
                astr += ','
            fout.write(astr)

    def _yield_plane_list_entries(self):
        query = self.session.query(func.count(Route.id), Plane, Airline, PlaneModel).join(Route.plane)
        query = query.join(Plane.airline).join(Plane.model).group_by(Plane.id)
        query = query.order_by(PlaneModel.name, Airline.name, Plane.tail_number)
        for count, plane, airline, model in query.all():
            results = list()
            results.append((model.name, True))  # True for protection mode
            results.append((airline.name, True))
            results.append((plane.tail_number, True))
            results.append((count, False))
            yield results

    def save_plane_list_csv(self):
        logger.info('Begin saving all planes.')
        start_time = time.clock()
        with open(self._get_stats_full_path('planes.csv'), 'w', encoding='utf8') as fout:
            fout.write('\ufeff')
            [fout.write('{:s},'.format(x)) for x in self.plane_fields]
            fout.write('\n')
            for result in self._yield_plane_list_entries():
                self._write_lists_to_csv(fout, result)
                fout.write("\n")
        logger.info('Finished saving all routes (time used is {:f}s)'.format(time.clock() - start_time))

    def save_all_stats(self):
        self.save_plane_list_csv()

import os
import time
from sqlalchemy import func

from .configs import logger
from .publicdata import ShmPublicDataApp, get_public_data_app

from .dbdefs import Route, Departure, Arrival, Station
from .dbops import ShmDbOps, get_shm_db_ops
from .dbops import get_configs


class ShmStationStats(object):
    def __init__(self):
        self.configs = get_configs()
        self.save_folder = self.configs.stats_folder
        self.dbops: ShmDbOps = get_shm_db_ops()
        self.session = self.dbops.session
        self.data_app: ShmPublicDataApp = get_public_data_app()
        self.station_fields = ['seq', 'sn', 'name', 'departures', 'arrivals']

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

    def _yield_station_list_entries(self):
        query_dep = self.session.query(Station, func.count(Departure.id)).select_from(Station)
        query_dep = query_dep.outerjoin(Departure).group_by(Station.id).order_by(Station.sn)
        query_arr = self.session.query(Station, func.count(Arrival.id)).select_from(Station)
        query_arr = query_arr.outerjoin(Arrival).group_by(Station.id).order_by(Station.sn)
        for (station, dep_num), (_, arr_num) in zip(query_dep.all(), query_arr.all()):
            results = list()
            results.append(station.sn)
            results.append(station.chn_name)
            results.append(dep_num)
            results.append(arr_num)
            yield results

    def save_station_list_csv(self):
        logger.info('Begin saving all stations.')
        start_time = time.clock()
        with open(self._get_stats_full_path('stations.csv'), 'w', encoding='utf8') as fout:
            fout.write('\ufeff')
            [fout.write('{:s},'.format(x)) for x in self.station_fields]
            fout.write('\n')
            for idx, result in enumerate(self._yield_station_list_entries()):
                fout.write('{:d},'.format(idx + 1))
                self._write_lists_to_csv(fout, result)
                fout.write('\n')
        logger.info('Finished saving all stations (time used is {:f}s)'.format(time.clock() - start_time))

    def save_all_stats(self):
        self.save_station_list_csv()

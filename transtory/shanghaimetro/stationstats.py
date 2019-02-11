import os
import time
from sqlalchemy import func

from .configs import logger
from .publicdata import ShmPublicDataApp, get_public_data_app

from .dbdefs import Route, Departure, Arrival
from .dbdefs import Train, TrainType, Line
from .dbops import ShmDbOps, get_shm_db_ops
from .dbops import ShmSysConfigs, get_configs
from .dbops import DateTimeHelper, get_datetime_helper


class ShmStationStats(object):
    def __init__(self):
        self.configs = get_configs()
        self.save_folder = self.configs.stats_folder
        self.dbops: ShmDbOps = get_shm_db_ops()
        self.session = self.dbops.session
        self.data_app: ShmPublicDataApp = get_public_data_app()
        self.station_fields = ['name', 'line', 'departure', 'arrival']

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
        query = self.session.query(func.count(Route.id), Train, TrainType).join(Route.train).join(Train.train_type)
        query = query.group_by(Train.id).order_by(Train.sn)
        for count, train, train_type in query.all():
            results = list()
            results.append(train.sn)
            results.append(train.status)
            results.append(train_type.name)
            results.append(count)
            results.append(train_type.maker)
            yield results

    def save_station_list_csv(self):
        logger.info('Begin saving all planes.')
        start_time = time.clock()
        with open(self._get_stats_full_path('trains.csv'), 'w', encoding='utf8') as fout:
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

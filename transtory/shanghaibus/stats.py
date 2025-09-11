import os
import time
from sqlalchemy import func

from .configs import logger
from .configs import get_configs
from .dbdefs import ShbDbModel
from .dbdefs import BusBrand, BusType, Company
from .dbdefs import BusTypeCompany
from .dbops import get_db_ops, ShbDbOps


class ShbStats(object):
    def __init__(self):
        self.configs = get_configs()
        self.save_folder = self.configs.stats_folder
        self.dbops: ShbDbOps = get_db_ops()
        self.session = self.dbops.session
        self.station_fields = ['seq', 'company', 'brand', 'code', 'model']

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

    def _yield_bus_type_entries(self):
        query = self.session.query(BusTypeCompany)
        for record in query.all():
            results = list()
            results.append(record.company.name)
            results.append(record.bus_type.brand.name)
            results.append(record.model)
            results.append(record.bus_type.type)
            yield results

    def save_bus_type_list_csv(self):
        logger.info('Begin saving all bus types.')
        start_time = time.perf_counter()
        with open(self._get_stats_full_path('bus_types.csv'), 'w', encoding='utf8') as fout:
            fout.write('\ufeff')
            [fout.write('{:s},'.format(x)) for x in self.station_fields]
            fout.write('\n')
            for idx, result in enumerate(self._yield_bus_type_entries()):
                fout.write('{:d},'.format(idx + 1))
                self._write_lists_to_csv(fout, result)
                fout.write('\n')
        logger.info('Finished saving all bus types (time used is {:f}s)'.format(time.perf_counter() - start_time))

    def save_all_stats(self):
        self.save_bus_type_list_csv()

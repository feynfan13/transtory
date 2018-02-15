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


class ShmTrainStats(object):
    def __init__(self):
        self.configs = get_configs()
        self.save_folder = self.configs.stats_folder
        self.dbops: ShmDbOps = get_shm_db_ops()
        self.session = self.dbops.session
        self.data_app: ShmPublicDataApp = get_public_data_app()
        self.train_fields = ["train", "model", "count", "manufacturer"]

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

    def _def_train_list_query(self):
        columns = ["line", "sn", "type"]
        query = self.session.query(Line.name, Train.sn, TrainType.name)
        query = query.join(Line.trains).join(Train.train_type).order_by(Train.sn)
        return columns, query

    def validate_train_type(self):
        validate_pass = True
        logger.info("Begin validating train types.")
        start_time = time.clock()
        columns, query = self._def_train_list_query()
        for train in query.all():
            train_sn, type_from_db = train[1], train[2]
            line, seq = self.data_app.get_line_and_seq_from_train_sn(train_sn)
            type_from_app = self.data_app.get_type_of_train(line, seq)
            logger.info("Train {:s}: {:s} passed".format(train_sn, type_from_db))
            if type_from_app != train[2]:
                validate_pass = False
                logger.warning("Train type from shanghai metro public data app and database do NOT match!")
                logger.warning("\tfor train {:s}: app {:s}, database {:s}".format(train_sn, type_from_app,
                                                                                  type_from_db))
        if validate_pass:
            logger.info("All trains have matching type with public data app match.")
        else:
            logger.warning("Validation of train type failed.")
        logger.info("Finished validating train types (time used is {:f}s)".format(time.clock() - start_time))

    def _yield_train_list_entries(self):
        query = self.session.query(func.count(Route.id), Train, TrainType).join(Route.train).join(Train.train_type)
        query = query.group_by(Train.id).order_by(Train.sn)
        for count, train, train_type in query.all():
            results = list()
            results.append(train.sn)
            results.append(train_type.name)
            results.append(count)
            results.append(train_type.maker)
            yield results

    def save_train_list_csv(self):
        logger.info("Begin saving all planes.")
        start_time = time.clock()
        with open(self._get_stats_full_path("trains.csv"), "w", encoding="utf16") as fout:
            [fout.write("|{:s}|\t".format(x)) for x in self.train_fields]
            fout.write("\n")
            for result in self._yield_train_list_entries():
                self._write_lists_to_csv(fout, result)
                fout.write("\n")
        logger.info("Finished saving all routes (time used is {:f}s)".format(time.clock() - start_time))

    def save_all_stats(self):
        self.validate_train_type()
        self.save_train_list_csv()

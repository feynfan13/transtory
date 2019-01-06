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
        self.train_fields = ['seq', 'train', 'model', 'count', 'manufacturer']
        self.train_type_fields = ['seq', 'type', 'taken', 'miss', 'total', 'ratio']

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
            # line, seq = self.data_app.get_line_and_seq_from_train_sn(train_sn)
            type_from_app = self.data_app.get_type_of_train(train_sn)
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
        logger.info('Begin saving all planes.')
        start_time = time.clock()
        with open(self._get_stats_full_path('trains.csv'), 'w', encoding='utf8') as fout:
            fout.write('\ufeff')
            [fout.write('{:s},'.format(x)) for x in self.train_fields]
            fout.write('\n')
            for idx, result in enumerate(self._yield_train_list_entries()):
                fout.write('{:d},'.format(idx + 1))
                self._write_lists_to_csv(fout, result)
                fout.write('\n')
        logger.info("Finished saving all routes (time used is {:f}s)".format(time.clock() - start_time))

    def _yield_train_type_list_entries(self):
        all_train_types = self.data_app.get_train_type_list()
        query = self.session.query(Train.train_type_id, func.count('*').label("count")).group_by(Train.train_type_id)
        stmt = query.subquery()
        query = self.session.query(TrainType, stmt.c.count).outerjoin(stmt, TrainType.id == stmt.c.train_type_id)
        query = query.order_by(TrainType.name)
        all_type_total, all_type_taken = 0, 0
        for train_type, count in query.all():
            name = train_type.name
            count = 0 if count is None else count
            total = int(all_train_types[name])
            results = list()
            results.append(name)
            results.append(count)
            results.append(total - count)
            results.append(total)
            results.append('{:d}%'.format(int(count*100.0/total)))
            all_type_total += total
            all_type_taken += count
            yield results
        results = list()
        results.append("Sum")
        results.append(all_type_taken)
        results.append(all_type_total)
        results.append("{:d}%".format(int(all_type_taken*100.0/all_type_total)))
        yield results

    def save_train_type_list_csv(self):
        logger.info('Begin saving all planes.')
        start_time = time.clock()
        with open(self._get_stats_full_path("train_type.csv"), "w", encoding="utf8") as fout:
            fout.write('\ufeff')
            [fout.write('{:s},'.format(x)) for x in self.train_type_fields]
            fout.write('\n')
            for idx, result in enumerate(self._yield_train_type_list_entries()):
                fout.write('{:d},'.format(idx + 1))
                self._write_lists_to_csv(fout, result)
                fout.write('\n')
        logger.info('Finished saving all routes (time used is {:f}s)'.format(time.clock() - start_time))

    def _yield_line_list_entries(self):
        query = self.session.query(func.count(Route.id), Train, TrainType).join(Route.train).join(Train.train_type)
        query = query.group_by(Train.id).order_by(Train.sn)
        for count, train, train_type in query.all():
            results = list()
            results.append(train.sn)
            results.append(train_type.name)
            results.append(count)
            results.append(train_type.maker)
            yield results

    def save_line_list_csv(self):
        logger.info('Begin saving all planes.')
        start_time = time.clock()
        with open(self._get_stats_full_path('trains.csv'), 'w', encoding='utf8') as fout:
            fout.write('\ufeff')
            [fout.write('|{:s}|,'.format(x)) for x in self.train_fields]
            fout.write('\n')
            for idx, result in enumerate(self._yield_train_list_entries()):
                fout.write('{:d},'.format(idx + 1))
                self._write_lists_to_csv(fout, result)
                fout.write('\n')
        logger.info("Finished saving all routes (time used is {:f}s)".format(time.clock() - start_time))

    def generate_unmet_train_str(self):
        train_set = set()
        for train_tp in self.session.query(Train.sn).all():
            train = train_tp[0]
            train_set.add(train)
        train_df = self.data_app.get_train_df()
        line_list = self.data_app.get_line_list()
        output_str = ''
        for line in line_list:
            output_str += "Line {:s}: ".format(line)
            train_of_line = train_df[train_df["line"] == line]
            for _, sr_train in train_of_line.iterrows():
                if sr_train["train"] not in train_set:
                    _, train_seq = self.data_app.get_line_and_seq_from_train_sn(sr_train["train"])
                    output_str += "{:d}, ".format(train_seq)
            output_str += "\n"
        return output_str

    def save_all_stats(self):
        self.validate_train_type()
        self.save_train_list_csv()
        self.save_train_type_list_csv()
        # self.save_line_list_csv()
        print(self.generate_unmet_train_str())

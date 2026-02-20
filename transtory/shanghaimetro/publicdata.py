import os
import json
import pandas as pd

from transtory.common import singleton
from .configs import get_configs, ShmSysConfigs


class ShmPublicData(object):
    """Public data, including
        -- Lines
        -- Stations
        -- Trains
    """

    def __init__(self):
        self.public_data_json = os.path.sep.join([os.path.dirname(__file__), 'publicdata.json'])
        self.train_vs_type = None

    def get_train_vs_type_table(self):
        if self.train_vs_type is None:
            self.train_vs_type = self._make_train_vs_type_table()
        return self.train_vs_type

    @staticmethod
    def _get_seq_list(train_type_json):
        train_sn_list = []
        id = train_type_json['sn_id']
        digits = train_type_json.get('sn_digits', 3)
        seq_list = train_type_json['sn_range']
        gen = train_type_json.get('generation', 0)
        assert (len(seq_list) % 2 == 0)
        num_pairs = int(len(seq_list) / 2)
        for idx_pair in range(num_pairs):
            seq_0 = seq_list[idx_pair * 2]
            seq_1 = seq_list[idx_pair * 2 + 1]
            assert (seq_0 <= seq_1)
            for idx in range(seq_0, seq_1 + 1):
                sn = '{:s}{num:0{width}}'.format(id, num=idx, width=digits)
                if gen != 0:
                    sn += '-{:d}'.format(gen)
                train_sn_list.append(sn)
        return train_sn_list

    def _make_train_vs_type_table(self):
        with open(self.public_data_json) as json_file:
            json_data = json.loads(json_file.read())
        train_list = []
        line_list = []
        type_list = []
        for line in json_data['all_trains']:
            for train_type in line['train_types']:
                trains_of_type = self._get_seq_list(train_type)
                for train in trains_of_type:
                    train_list.append(train)
                    line_list.append(line['line'])
                    type_list.append(train_type['train_type'])

        train_vs_type_df = pd.DataFrame.from_dict(data={'train': train_list, 'line': line_list, 'type': type_list})
        train_vs_type_df.index = train_vs_type_df['train']
        return train_vs_type_df


get_public_data = singleton(ShmPublicData)


class ShmPublicDataApp(object):
    instance = None

    def __init__(self):
        self.public_data: ShmPublicData = get_public_data()

    @classmethod
    def get_instance(cls):
        if cls.instance is None:
            cls.instance = ShmPublicDataApp()
        return cls.instance

    def get_type_of_train(self, train_sn):
        query_table = self.public_data.get_train_vs_type_table()
        # Include the case of updated trains
        if '-' in train_sn:
            train_sn = train_sn.split('-')[0]
        return query_table.loc[train_sn, 'type']

    def get_train_type_list(self):
        train_table = self.public_data.get_train_vs_type_table()
        train_type_list = train_table.groupby(by='type')['train'].count()
        return train_type_list

    def get_train_df(self):
        return self.public_data.train_vs_type

    def get_line_list(self):
        train_table = self.public_data.get_train_vs_type_table()
        line_list = train_table['line'].unique()
        return line_list

    def get_trains_of_line(self, line_str):
        train_df = self.public_data.get_train_vs_type_table()
        return train_df[train_df['line'] == int(line_str)]

    @staticmethod
    def get_train_sn(line: str, seq: int):
        """Get train sn from line and number in line
        Before 2017-12, number takes two digits, such as 0101.
        Currently, with expanding rolling stocks and lines, number can be
          -- for main lines, 2-digit line number + 3-digit train sequence number, such as 01001.
          -- for minor lines, 3-alphadigit line number + 3-digit train sequence number, such as T01001.
        """
        # return "{:2d}{:2d}".format(line, number)
        return '{:s}{:3d}'.format(line, seq)


get_public_data_app = singleton(ShmPublicDataApp)

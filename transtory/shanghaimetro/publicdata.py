import pandas as pd

from transtory.common import singleton


class ShmPublicData(object):
    """Public data, including
        -- Lines
        -- Stations
        -- Trains
    """
    def __init__(self):
        self.train_vs_type = None

    @staticmethod
    def _get_train_sn_from_line_and_seq(line, seq, gen=None):
        if gen is None:
            return '{:s}{:03d}'.format(line, seq)
        else:
            return '{:s}{:03d}-{:02d}'.format(line, seq, gen)

    def _add_train_and_type_in_sn_range(self, line, train_type: str, sn_range, gen=None):
        seq_list = range(sn_range[0], sn_range[1] + 1)
        for seq in seq_list:
            self.train_line_type_list[0].append(self._get_train_sn_from_line_and_seq(line, seq, gen))
            self.train_line_type_list[1].append(line)
            self.train_line_type_list[2].append(train_type)

    def get_train_vs_type_table(self):
        if self.train_vs_type is None:
            self.train_vs_type = self._make_train_vs_type_table()
        return self.train_vs_type

    def _make_train_vs_type_table(self):
        self.train_line_type_list = [[], [], []]
        # Line 01
        self._add_train_and_type_in_sn_range('01', "01A01-01", (1, 1))
        self._add_train_and_type_in_sn_range('01', "01A01-02", (2, 2))
        self._add_train_and_type_in_sn_range('01', "01A01-01", (3, 10))
        self._add_train_and_type_in_sn_range('01', "01A03", (11, 13))
        self._add_train_and_type_in_sn_range('01', "01A01-01", (14, 14))
        self._add_train_and_type_in_sn_range('01', "01A03", (15, 16))
        self._add_train_and_type_in_sn_range('01', "01A02-02", (17, 17))
        self._add_train_and_type_in_sn_range('01', "01A02-01", (18, 25))
        self._add_train_and_type_in_sn_range('01', "01A04-01", (26, 29))
        self._add_train_and_type_in_sn_range('01', "01A04-02", (30, 37))
        self._add_train_and_type_in_sn_range('01', "01A05", (40, 55))
        self._add_train_and_type_in_sn_range('01', "01A06", (56, 66))
        self._add_train_and_type_in_sn_range('01', "01A06", (67, 86))
        # Line 02
        self._add_train_and_type_in_sn_range('02', '02A01', (1, 16))
        self._add_train_and_type_in_sn_range('02', '02A02', (33, 53))
        self._add_train_and_type_in_sn_range('02', '02A03', (54, 69))
        self._add_train_and_type_in_sn_range('02', '02A04-01', (70, 85), 1)
        self._add_train_and_type_in_sn_range('02', '02A04', (70, 85))
        self._add_train_and_type_in_sn_range('02', '02A05', (86, 116))
        # Line 03
        self._add_train_and_type_in_sn_range('03', "03A01", (1, 28))
        self._add_train_and_type_in_sn_range('03', "03A02&04A02", (29, 36))
        #   Train 37-49 is borrowed from Line 04 and patched to 03xxx
        #   We use 04xxx when registering the respective trips
        # Line 04
        self._add_train_and_type_in_sn_range('04', "04A01", (1, 2))  # Siemens
        self._add_train_and_type_in_sn_range('04', "04A01", (3, 28))  # 南车株洲
        self._add_train_and_type_in_sn_range('04', "03A02&04A02", (29, 29))  # 中车长春
        self._add_train_and_type_in_sn_range('04', "03A02&04A02", (30, 36))  # Alstom上海
        self._add_train_and_type_in_sn_range('04', "03A02&04A02", (37, 49))  # Alstom上海
        self._add_train_and_type_in_sn_range('04', "03A02&04A02", (50, 55))  # Alstom上海
        # Line 05
        self._add_train_and_type_in_sn_range('05', "05C01", (1, 13))
        self._add_train_and_type_in_sn_range('05', "05C01", (15, 18))
        self._add_train_and_type_in_sn_range('05', "05C02", (19, 51))
        # Line 06
        self._add_train_and_type_in_sn_range('06', "06C01", (1, 3))
        self._add_train_and_type_in_sn_range('06', "06C01", (5, 13))
        self._add_train_and_type_in_sn_range('06', "06C01", (15, 23))
        self._add_train_and_type_in_sn_range('06', "06C02", (25, 33))
        self._add_train_and_type_in_sn_range('06', "06C02", (35, 36))
        self._add_train_and_type_in_sn_range('06', "06C03", (37, 43))
        self._add_train_and_type_in_sn_range('06', "06C03", (45, 53))
        self._add_train_and_type_in_sn_range('06', "06C03", (55, 56))
        # Line 07
        self._add_train_and_type_in_sn_range('07', "07A01", (1, 42))
        self._add_train_and_type_in_sn_range('07', "07A02", (43, 72))
        # Line 08
        self._add_train_and_type_in_sn_range('08', "08C01", (1, 28))
        self._add_train_and_type_in_sn_range('08', "08C02", (29, 45))
        self._add_train_and_type_in_sn_range('08', "08C03", (46, 66))
        # Line 09
        self._add_train_and_type_in_sn_range('09', "09A01", (1, 10))
        self._add_train_and_type_in_sn_range('09', "09A02", (11, 51))
        self._add_train_and_type_in_sn_range('09', "09A03", (53, 88))
        # Line 10
        self._add_train_and_type_in_sn_range('10', "10A01", (1, 41))
        self._add_train_and_type_in_sn_range('10', "10A02", (42, 67))
        # Line 11
        self._add_train_and_type_in_sn_range('11', "11A01", (1, 66))
        self._add_train_and_type_in_sn_range('11', "11A02", (67, 72))
        self._add_train_and_type_in_sn_range('11', "11A03", (73, 82))
        # Line 12
        self._add_train_and_type_in_sn_range('12', "12A01", (1, 41))
        self._add_train_and_type_in_sn_range('12', "12A02", (42, 56))
        # Line 13
        self._add_train_and_type_in_sn_range('13', "13A01", (1, 24))
        self._add_train_and_type_in_sn_range('13', "13A02", (25, 62))
        # Line 16
        self._add_train_and_type_in_sn_range('16', "16A01", (1, 46))
        # Line 17
        self._add_train_and_type_in_sn_range('17', "17A01", (1, 5))
        self._add_train_and_type_in_sn_range('17', "17A01", (6, 28))
        # Line T01
        self._add_train_and_type_in_sn_range('T01', 'APM300', (1, 11))

        train_vs_type_df = pd.DataFrame.from_dict(data={'train': self.train_line_type_list[0],
                                                        'line': self.train_line_type_list[1],
                                                        'type': self.train_line_type_list[2]})
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

    @staticmethod
    def get_line_and_seq_from_train_sn(train_sn):
        if train_sn[0].isalpha():  # minor lines, such as APM
            sep_loc = 3
        else:  # main lines, such as Line 1
            sep_loc = 2
        return train_sn[0:sep_loc], int(train_sn[sep_loc:])


get_public_data_app = singleton(ShmPublicDataApp)

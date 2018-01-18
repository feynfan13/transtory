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
    def _add_train_and_type_in_sn_range(train_dict, train_type: str, sn_range):
        seq_list = range(sn_range[0], sn_range[1] + 1)
        for seq in seq_list:
            train_dict[seq] = train_type

    def get_train_vs_type_table(self):
        if self.train_vs_type is None:
            self.train_vs_type = self._make_train_vs_type_table()
        return self.train_vs_type

    def _make_train_vs_type_table(self):
        train_vs_type_table = dict()
        # Line 01
        line_01_dict = dict()
        self._add_train_and_type_in_sn_range(line_01_dict, "01A01-01", (1, 1))
        self._add_train_and_type_in_sn_range(line_01_dict, "01A01-02", (2, 2))
        self._add_train_and_type_in_sn_range(line_01_dict, "01A01-01", (3, 10))
        self._add_train_and_type_in_sn_range(line_01_dict, "01A03", (11, 13))
        self._add_train_and_type_in_sn_range(line_01_dict, "01A01-01", (14, 14))
        self._add_train_and_type_in_sn_range(line_01_dict, "01A03", (15, 16))
        self._add_train_and_type_in_sn_range(line_01_dict, "01A02-02", (17, 17))
        self._add_train_and_type_in_sn_range(line_01_dict, "01A02-01", (18, 25))
        self._add_train_and_type_in_sn_range(line_01_dict, "01A04-01", (26, 29))
        self._add_train_and_type_in_sn_range(line_01_dict, "01A04-02", (30, 37))
        self._add_train_and_type_in_sn_range(line_01_dict, "01A05", (40, 55))
        self._add_train_and_type_in_sn_range(line_01_dict, "01A06", (56, 66))
        self._add_train_and_type_in_sn_range(line_01_dict, "01A06", (67, 86))
        train_vs_type_table[1] = line_01_dict
        # Line 02
        line_02_dict = dict()
        self._add_train_and_type_in_sn_range(line_02_dict, "02A01", (1, 16))
        self._add_train_and_type_in_sn_range(line_02_dict, "02A02", (33, 53))
        self._add_train_and_type_in_sn_range(line_02_dict, "02A03", (54, 69))
        self._add_train_and_type_in_sn_range(line_02_dict, "02A04", (70, 85))
        train_vs_type_table[2] = line_02_dict
        # Line 03
        line_03_dict = dict()
        self._add_train_and_type_in_sn_range(line_03_dict, "03A01", (1, 28))
        self._add_train_and_type_in_sn_range(line_03_dict, "03A02&04A02", (29, 42))
        train_vs_type_table[3] = line_03_dict
        # Line 04
        line_04_dict = dict()
        self._add_train_and_type_in_sn_range(line_04_dict, "04A01", (1, 28))
        self._add_train_and_type_in_sn_range(line_04_dict, "03A02&04A02", (29, 44))
        train_vs_type_table[4] = line_04_dict
        # Line 05
        line_05_dict = dict()
        self._add_train_and_type_in_sn_range(line_05_dict, "05C01", (1, 17))
        train_vs_type_table[5] = line_05_dict
        # Line 06
        line_06_dict = dict()
        self._add_train_and_type_in_sn_range(line_06_dict, "06C01", (1, 3))
        self._add_train_and_type_in_sn_range(line_06_dict, "06C01", (5, 13))
        self._add_train_and_type_in_sn_range(line_06_dict, "06C01", (15, 23))
        self._add_train_and_type_in_sn_range(line_06_dict, "06C02", (25, 33))
        self._add_train_and_type_in_sn_range(line_06_dict, "06C02-01", (35, 36))
        self._add_train_and_type_in_sn_range(line_06_dict, "06C03", (37, 43))
        self._add_train_and_type_in_sn_range(line_06_dict, "06C03", (45, 53))
        self._add_train_and_type_in_sn_range(line_06_dict, "06C03", (55, 56))
        train_vs_type_table[6] = line_06_dict
        # Line 07
        line_07_dict = dict()
        self._add_train_and_type_in_sn_range(line_07_dict, "07A01", (1, 42))
        train_vs_type_table[7] = line_07_dict
        # Line 08
        line_08_dict = dict()
        self._add_train_and_type_in_sn_range(line_08_dict, "08C01", (1, 28))
        self._add_train_and_type_in_sn_range(line_08_dict, "08C02", (29, 45))
        self._add_train_and_type_in_sn_range(line_08_dict, "08C03", (46, 66))
        train_vs_type_table[8] = line_08_dict
        # Line 09
        line_09_dict = dict()
        self._add_train_and_type_in_sn_range(line_09_dict, "09A01", (1, 10))
        self._add_train_and_type_in_sn_range(line_09_dict, "09A02", (11, 51))
        self._add_train_and_type_in_sn_range(line_09_dict, "09A03", (54, 89))
        train_vs_type_table[9] = line_09_dict
        # Line 10
        line_10_dict = dict()
        self._add_train_and_type_in_sn_range(line_10_dict, "10A01", (1, 41))
        train_vs_type_table[10] = line_10_dict
        # Line 11
        line_11_dict = dict()
        self._add_train_and_type_in_sn_range(line_11_dict, "11A01", (1, 66))
        self._add_train_and_type_in_sn_range(line_11_dict, "11A02", (67, 72))
        self._add_train_and_type_in_sn_range(line_11_dict, "11A03", (73, 82))
        train_vs_type_table[11] = line_11_dict
        # Line 12
        line_12_dict = dict()
        self._add_train_and_type_in_sn_range(line_12_dict, "12A01", (1, 41))
        self._add_train_and_type_in_sn_range(line_12_dict, "12A02", (42, 56))
        train_vs_type_table[12] = line_12_dict
        # Line 13
        line_13_dict = dict()
        self._add_train_and_type_in_sn_range(line_13_dict, "13A01", (1, 24))
        self._add_train_and_type_in_sn_range(line_13_dict, "13A02", (25, 62))
        train_vs_type_table[13] = line_13_dict
        # Line 16
        line_16_dict = dict()
        self._add_train_and_type_in_sn_range(line_16_dict, "16A01", (1, 46))
        train_vs_type_table[16] = line_16_dict
        # Line 17
        line_17_dict = dict()
        self._add_train_and_type_in_sn_range(line_17_dict, "17A01", (1, 5))
        self._add_train_and_type_in_sn_range(line_17_dict, "17A01", (6, 28))
        train_vs_type_table[17] = line_17_dict
        return train_vs_type_table


get_public_data = singleton(ShmPublicData)


class ShmPublicDataApp(object):
    def __init__(self):
        self.public_data: ShmPublicData = get_public_data()

    def get_type_of_train(self, line, seq):
        query_table = self.public_data.get_train_vs_type_table()
        return query_table[line][seq]

    @staticmethod
    def get_train_sn(line: int, seq: int):
        """Get train sn from line and number in line
        Before 2017-12, number takes two digits, such as 0101.
        Currently, with expanding rolling stocks, number takes three digits, such as 01001.
        """
        # return "{:2d}{:2d}".format(line, number)
        return "{:2d}{:3d}".format(line, seq)

    @staticmethod
    def get_line_and_seq_from_train_sn(train_sn):
        return int(train_sn[:2]), int(train_sn[2:])


get_public_data_app = singleton(ShmPublicDataApp)

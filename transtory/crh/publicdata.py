import os
import xml.etree.ElementTree as ET
from lxml import etree

from transtory.common import singleton
from .configs import CrhSysConfigs, get_configs


class CrhPublicData(object):
    """Public data, including
        -- Train types
        -- Train type query table
    """
    def __init__(self):
        public_data_xml = os.path.sep.join([os.path.dirname(__file__), 'publicdata.xml'])
        public_data_root = ET.parse(public_data_xml).getroot()
        self.train_type_tree = public_data_root.find('train_type')
        self.type_vs_train = dict()
        for train_type in self.train_type_tree.iter('level3'):
            name = train_type.attrib['name']
            sn_set = set()
            for sn_range_record in train_type.iter('sn_range'):
                sn_range = sn_range_record.text.split()
                sn_start, sn_end = int(sn_range[0]), int(sn_range[1])
                for sn in range(sn_start, sn_end + 1):
                    sn_set.add(sn)
            self.type_vs_train[name] = sn_set

    def get_train_type_tree(self):
        """Get the train type hierarchy in xml ElementTree style.
        Currently, a 4-level tree is used to organize the train types, which are
            * level 0: for eras/grades, including CRH, CRH380, CR400
            * level 1: for models/manufacturers. For example, for CRH, there are CRH1, CRH2, CRH3, CRH5, CRH6, etc.
            * level 2: for variants. For example, for CRH2, there are CRH2A, CRH2B, CRH2E, CRH2G, etc.
            * level 3: for design improvements. For example, for CRH2E, there are 初代 and 2G头型
        The hierarchy system is not official and are prone to changes.
        """
        return self.train_type_tree

    def get_train_type_and_train_map(self):
        return self.type_vs_train


get_public_data = singleton(CrhPublicData)


class CrhPublicDataApp(object):
    def __init__(self):
        self.public_data: CrhPublicData = get_public_data()
        self.configs: CrhSysConfigs = get_configs()

    def _get_stats_full_path(self, fname):
        return os.path.sep.join([self.configs.stats_folder, fname])

    @staticmethod
    def _get_type_and_seq_from_train_sn(train_sn):
        return train_sn[:-5], int(train_sn[-4:])

    def save_train_type_tree(self):
        fpath = self._get_stats_full_path("all_train_types.xml")
        xml_tree = self.public_data.get_train_type_tree()
        xml_tree.write(fpath)
        lxml_tree = etree.parse(fpath)
        with open(fpath, "wb") as fout:
            fout.write(etree.tostring(lxml_tree, encoding='UTF-8', xml_declaration=True, pretty_print=True))

    def get_train_type(self, train_sn):
        l2_name, seq = self._get_type_and_seq_from_train_sn(train_sn)
        xml_tree = self.public_data.get_train_type_tree()
        type_vs_train = self.public_data.get_train_type_and_train_map()
        type_str = ''
        for level2 in xml_tree.iter('level2'):
            if level2.attrib['name'] == l2_name:
                for level3 in level2.iter('level3'):
                    l3_name = level3.attrib['name']
                    if seq in type_vs_train[l3_name]:
                        type_str = l3_name
                        break
                break
        if len(type_str) == 0:
            err_msg = 'Train {:s} is not in public data list.'.format(train_sn)
            raise Exception(err_msg)
        return type_str

    def get_train_count_from_type(self, train_type):
        type_vs_train = self.public_data.get_train_type_and_train_map()
        if train_type in type_vs_train:
            return len(type_vs_train[train_type])
        else:
            return 0

    def save_public_data(self):
        self.save_train_type_tree()


get_public_data_app = singleton(CrhPublicDataApp)


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
        self.train_type_tree = None
        self.type_vs_train = None

    def get_train_type_tree(self):
        """Get the train type hierarchy in xml ElementTree style.
        Currently a 4-level tree is used to organize the train types, which are
            * level 0: for eras/grades, including CRH, CRH380, CR400
            * level 1: for models/manufacturers. For example, for CRH, there are CRH1, CRH2, CRH3, CRH5, CRH6, etc.
            * level 2: for variants. For example, for CRH2, there are CRH2A, CRH2B, CRH2E, CRH2G, etc.
            * level 3: for design improvements. For example, for CRH2E, there are 初代 and 2G头型
        The hierarchy system is not official and are prone to changes.
        """
        if self.train_type_tree is not None:
            return self.train_type_tree
        root = ET.Element("train_type")
        # Level 0
        ET.SubElement(root, "level0", name="CRH")
        ET.SubElement(root, "level0", name="CRH380")
        ET.SubElement(root, "level0", name="CR400")
        # Level 1
        for level0 in root.iter("level0"):
            name = level0.attrib["name"]
            if name == "CRH":
                ET.SubElement(level0, "level1", name="CRH1")
                ET.SubElement(level0, "level1", name="CRH2")
                ET.SubElement(level0, "level1", name="CRH3")
                ET.SubElement(level0, "level1", name="CRH5")
                ET.SubElement(level0, "level1", name="CRH6")
            elif name == "CRH380":
                ET.SubElement(level0, "level1", name="CRH380A")
                ET.SubElement(level0, "level1", name="CRH380B")
                ET.SubElement(level0, "level1", name="CRH380C")
                ET.SubElement(level0, "level1", name="CRH380D")
            elif name == "CR400":
                ET.SubElement(level0, "level1", name="CR400AF")
                ET.SubElement(level0, "level1", name="CR400BF")
        # Level 2
        for level1 in root.iter("level1"):
            name = level1.attrib["name"]
            if name == "CRH1":
                ET.SubElement(level1, "level2", name="CRH1A")
                ET.SubElement(level1, "level2", name="CRH1A-A")
                ET.SubElement(level1, "level2", name="CRH1B")
                ET.SubElement(level1, "level2", name="CRH1E")
            elif name == "CRH2":
                ET.SubElement(level1, "level2", name="CRH2A")
                ET.SubElement(level1, "level2", name="CRH2B")
                ET.SubElement(level1, "level2", name="CRH2C")
                ET.SubElement(level1, "level2", name="CRH2E")
                ET.SubElement(level1, "level2", name="CRH2G")
            elif name == "CRH3":
                ET.SubElement(level1, "level2", name="CRH3A")
                ET.SubElement(level1, "level2", name="CRH3C")
            elif name == "CRH5":
                ET.SubElement(level1, "level2", name="CRH5A")
                ET.SubElement(level1, "level2", name="CRH5G")
            elif name == "CRH6":
                ET.SubElement(level1, "level2", name="CRH6A")
                ET.SubElement(level1, "level2", name="CRH6F")
            elif name == "CRH380A":
                ET.SubElement(level1, "level2", name="CRH380A")
                ET.SubElement(level1, "level2", name="CRH380AL")
            elif name == "CRH380B":
                ET.SubElement(level1, "level2", name="CRH380B")
                ET.SubElement(level1, "level2", name="CRH380BG")
                ET.SubElement(level1, "level2", name="CRH380BL")
            elif name == "CRH380C":
                ET.SubElement(level1, "level2", name="CRH380CL")
            elif name == "CRH380D":
                ET.SubElement(level1, "level2", name="CRH380D")
            elif name == "CR400AF":
                ET.SubElement(level1, "level2", name="CR400AF")
            elif name == "CR400BF":
                ET.SubElement(level1, "level2", name="CR400BF")
        # Level 3
        for level2 in root.iter("level2"):
            name = level2.attrib["name"]
            if name == "CRH1A":
                ET.SubElement(level2, "level3", name="CRH1A 200")
                ET.SubElement(level2, "level3", name="CRH1A 250")
            elif name == "CRH1A-A":
                ET.SubElement(level2, "level3", name="CRH1A-A")
            elif name == "CRH1B":
                ET.SubElement(level2, "level3", name="CRH1B")
                ET.SubElement(level2, "level3", name="CRH1B 1E头型")
            elif name == "CRH1E":
                ET.SubElement(level2, "level3", name="CRH1E")
                ET.SubElement(level2, "level3", name="CRH1E 1A-A头型_横向卧铺")
            elif name == "CRH2A":
                ET.SubElement(level2, "level3", name="CRH2A")
                ET.SubElement(level2, "level3", name="CRH2A 统型")
                ET.SubElement(level2, "level3", name="CRH2A 2G头型")
            elif name == "CRH2B":
                ET.SubElement(level2, "level3", name="CRH2B")
            elif name == "CRH2C":
                ET.SubElement(level2, "level3", name="CRH2C 第一阶段")
                ET.SubElement(level2, "level3", name="CRH2C 第二阶段")
            elif name == "CRH2E":
                ET.SubElement(level2, "level3", name="CRH2E")
                ET.SubElement(level2, "level3", name="CRH2E 2G头型")
            elif name == "CRH2G":
                ET.SubElement(level2, "level3", name="CRH2G")
            elif name == "CRH3A":
                ET.SubElement(level2, "level3", name="CRH3A")
            elif name == "CRH3C":
                ET.SubElement(level2, "level3", name="CRH3C")
            elif name == "CRH5A":
                ET.SubElement(level2, "level3", name="CRH5A")
                ET.SubElement(level2, "level3", name="CRH5A 第二代")
            elif name == "CRH5E":
                ET.SubElement(level2, "level3", name="CRH5A CJ1头型")
            elif name == "CRH5G":
                ET.SubElement(level2, "level3", name="CRH5G")
            elif name == "CRH380A":
                ET.SubElement(level2, "level3", name="CRH380A")
                ET.SubElement(level2, "level3", name="CRH380A 统型")
            elif name == "CRH380AL":
                ET.SubElement(level2, "level3", name="CRH380AL 第一阶段")
                ET.SubElement(level2, "level3", name="CRH380AL 第二阶段")
                ET.SubElement(level2, "level3", name="CRH380AL E35")
            elif name == "CRH380BL":
                ET.SubElement(level2, "level3", name="CRH380BL 第一阶段")
                ET.SubElement(level2, "level3", name="CRH380BL 第二阶段")
                ET.SubElement(level2, "level3", name="CRH380BL 第三阶段")
            elif name == "CRH380BG":
                ET.SubElement(level2, "level3", name="CRH380BG")
                ET.SubElement(level2, "level3", name="CRH380BG 统型")
            elif name == "CRH380B":
                ET.SubElement(level2, "level3", name="CRH380B 统型")
            elif name == "CRH380CL":
                ET.SubElement(level2, "level3", name="CRH380CL")
            elif name == "CRH380D":
                ET.SubElement(level2, "level3", name="CRH380D")
                ET.SubElement(level2, "level3", name="CRH380D 统型")
            elif name == "CR400AF":
                ET.SubElement(level2, "level3", name="CR400AF")
            elif name == "CR400BF":
                ET.SubElement(level2, "level3", name="CR400BF")

        xml_tree = ET.ElementTree(root)
        self.train_type_tree = xml_tree
        return xml_tree

    def get_train_type_and_train_map(self):
        if self.type_vs_train is not None:
            return self.type_vs_train
        xml_tree = self.get_train_type_tree if self.train_type_tree is None else self.train_type_tree

        def get_num_set_from_multiple_ranges(ranges):
            num_set = set()
            for current in ranges:
                [num_set.add(x) for x in range(current[0], current[1]+1)]
            return num_set

        type_train_map = dict()
        for train_type in xml_tree.getroot().iter("level3"):
            name = train_type.attrib["name"]
            if name == "CRH1A 200":
                sn_list = get_num_set_from_multiple_ranges([(1001, 1041)])
            elif name == "CRH1A 250":
                sn_list = get_num_set_from_multiple_ranges([(1081, 1168)])
            elif name == "CRH1A-A":
                sn_list = get_num_set_from_multiple_ranges([(1169, 1191), (1234, 1237)])
            elif name == "CRH1B":
                sn_list = get_num_set_from_multiple_ranges([(1041, 1045), (1047, 1060)])
            elif name == "CRH1B 1E头型":
                sn_list = get_num_set_from_multiple_ranges([(1076, 1080)])
            elif name == "CRH1E":
                sn_list = get_num_set_from_multiple_ranges([(1061, 1072), (1073, 1075)])
            elif name == "CRH1E 1A-A头型_横向卧铺":
                sn_list = get_num_set_from_multiple_ranges([(1229, 1233)])
            elif name == "CRH2A":
                sn_list = get_num_set_from_multiple_ranges([(2001, 2009), (2011, 2060), (2151, 2211)])
            elif name == "CRH2A 统型":
                sn_list = get_num_set_from_multiple_ranges([(2212, 2416), (2427, 2459), (2473, 2499),
                                                            (4001, 4071), (4082, 4095)])
            elif name == "CRH2A 2G头型":
                sn_list = get_num_set_from_multiple_ranges([(2460, 2460)])
            elif name == "CRH2B":
                sn_list = get_num_set_from_multiple_ranges([(2111, 2120)])
            elif name == "CRH2C 第一阶段":
                sn_list = get_num_set_from_multiple_ranges([(2062, 2067), (2069, 2090)])
            elif name == "CRH2C 第二阶段":
                sn_list = get_num_set_from_multiple_ranges([(2091, 2110), (2141, 2149)])
            elif name == "CRH2E":
                sn_list = get_num_set_from_multiple_ranges([(2121, 2138), (2140, 2140)])
            elif name == "CRH2E 2G头型":
                sn_list = get_num_set_from_multiple_ranges([(2461, 2472)])
            elif name == "CRH2G":
                sn_list = get_num_set_from_multiple_ranges([(2417, 2426), (4072, 4081)])
            elif name == "CRH3A":
                sn_list = get_num_set_from_multiple_ranges([(5218, 5218)])
            elif name == "CRH3C":
                sn_list = get_num_set_from_multiple_ranges([(3001, 3080)])
            elif name == "CRH5A":
                sn_list = get_num_set_from_multiple_ranges([(5001, 5013), (5044, 5055)])
            elif name == "CRH5A 第二代":
                sn_list = get_num_set_from_multiple_ranges([(5056, 5140)])
            elif name == "CRH5E":
                sn_list = get_num_set_from_multiple_ranges([(5201, 5205)])
            elif name == "CRH5G":
                sn_list = get_num_set_from_multiple_ranges([(5141, 5200), (5206, 5215)])
            elif name == "CRH380A":
                sn_list = get_num_set_from_multiple_ranges([(2501, 2537), (2539, 2540)])
            elif name == "CRH380A 统型":
                sn_list = get_num_set_from_multiple_ranges([(2641, 2807), (2809, 2817), (2819, 2827),
                                                            (2829, 2912), (2921, 2925)])
            elif name == "CRH380AL 第一阶段":
                sn_list = get_num_set_from_multiple_ranges([(2541, 2570)])
            elif name == "CRH380AL 第二阶段":
                sn_list = get_num_set_from_multiple_ranges([(2571, 2640)])
            elif name == "CRH380AL E35":
                sn_list = get_num_set_from_multiple_ranges([(2913, 2920)])
            elif name == "CRH380BL 第一阶段":
                sn_list = get_num_set_from_multiple_ranges([(3501, 3542), (5501, 5540)])
            elif name == "CRH380BL 第二阶段":
                sn_list = get_num_set_from_multiple_ranges([(3543, 3570), (5541, 5545)])
            elif name == "CRH380BL 第三阶段":
                sn_list = get_num_set_from_multiple_ranges([(3732, 3737), (5823, 5828)])
            elif name == "CRH380BG":
                sn_list = get_num_set_from_multiple_ranges([(5546, 5600), (5626, 5636)])
            elif name == "CRH380BG 统型":
                sn_list = get_num_set_from_multiple_ranges([(5684, 5729), (5762, 5786), (5803, 5822)])
            elif name == "CRH380B 统型":
                sn_list = get_num_set_from_multiple_ranges([(3571, 3731), (3738, 3774), (5637, 5683),
                                                            (5730, 5761), (5787, 5802), (5829, 5888)])
            elif name == "CRH380CL":
                sn_list = get_num_set_from_multiple_ranges([(5601, 5625)])
            elif name == "CRH380D":
                sn_list = get_num_set_from_multiple_ranges([(1501, 1510)])
            elif name == "CRH380D 统型":
                sn_list = get_num_set_from_multiple_ranges([(1511, 1585)])
            else:
                sn_list = []
            type_train_map[name] = sn_list
        self.type_vs_train = type_train_map
        return type_train_map


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
        type_str = ""
        for level2 in xml_tree.getroot().iter("level2"):
            if level2.attrib["name"] == l2_name:
                for level3 in level2.iter("level3"):
                    l3_name = level3.attrib["name"]
                    if seq in type_vs_train[l3_name]:
                        type_str = l3_name
                        break
                break
        return type_str

    def save_public_data(self):
        self.save_train_type_tree()
        # print(self.get_train_type("CRH2B-2118"))
        # print(self.get_train_type("CRH380BL-5535"))
        # print(self.get_train_type("CRH1A-A-1190"))


get_public_data_app = singleton(CrhPublicDataApp)


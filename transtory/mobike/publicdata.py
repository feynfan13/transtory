"""
Mobike public data, including bike types, subtypes, etc.
"""

import transtory.common as helpers


class MobikePublicData(object):
    """Public data, including
        -- bike types
        -- bike subtypes
    """
    def __init__(self):
        pass

    @staticmethod
    def get_bike_types():
        bike_types = list()
        # !!! DO NOT ALTER SEQUENCE !!!
        # Bike type name, bike type codename
        # 000: NA
        bike_types.append(["NA", ""])
        # 001: Classic 1.0
        bike_types.append(["Classic 1.x", ""])
        # 002: Classic 2.0
        bike_types.append(["Classic 2.x", ""])
        # 003: Classic 3.0
        bike_types.append(["Classic 3.x", "风轻扬"])
        # 004: Light 1.0
        bike_types.append(["Light 1.x", ""])
        # 005: Light 2.0
        bike_types.append(["Light 2.x", ""])
        return bike_types

    @staticmethod
    def get_bike_subtypes():
        bike_subtypes = list()
        # !!! DO NOT ALTER SEQUENCE !!!
        columns = ["bike_subtype_name, bike_type_name"]
        # NA
        bike_subtypes.append(["NA", "NA"])
        # Classic 1.0 (for unknown Classic 1.x bikes)
        bike_subtypes.append(["Classic 1.x", "Classic 1.x"])
        # Classic 1.1
        bike_subtypes.append(["Classic 1.1", "Classic 1.x"])
        # Classic 1.2
        bike_subtypes.append(["Classic 1.2", "Classic 1.x"])
        # Classic 2.x (for unknown Classic 2.x bikes)
        bike_subtypes.append(["Classic 2.x", "Classic 2.x"])
        # Classic 2.1
        bike_subtypes.append(["Classic 2.1", "Classic 2.x"])
        # Classic 2.2
        bike_subtypes.append(["Classic 2.2", "Classic 2.x"])
        # Classic 3.x
        bike_subtypes.append(["Classic 3.x", "Classic 3.x"])
        # Classic 3.1: metallic basket
        bike_subtypes.append(["Classic 3.1", "Classic 3.x"])
        # Classic 3.2: plastic basket; solar panel in basket
        bike_subtypes.append(["Classic 3.2", "Classic 3.x"])
        # Light 1.x
        bike_subtypes.append(["Light 1.x", "Light 1.x"])
        # Light 1.1
        bike_subtypes.append(["Light 1.1", "Light 1.x"])
        # Light 1.2
        bike_subtypes.append(["Light 1.2", "Light 1.x"])
        # Light 1.3
        bike_subtypes.append(["Light 1.3", "Light 1.x"])
        # Light 1.4
        bike_subtypes.append(["Light 1.4", "Light 1.x"])
        # Light 2.x
        bike_subtypes.append(["Light 2.x", "Light 2.x"])
        # Light 2.1
        bike_subtypes.append(["Light 2.1", "Light 2.x"])
        # Light 2.2
        bike_subtypes.append(["Light 2.2", "Light 2.x"])
        # Light 2.3
        bike_subtypes.append(["Light 2.3", "Light 2.x"])
        # Light 2.4
        bike_subtypes.append(["Light 2.4", "Light 2.x"])
        # Light 2.5
        bike_subtypes.append(["Light 2.5", "Light 2.x"])
        # Light 2.6
        bike_subtypes.append(["Light 2.6", "Light 2.x"])
        # Light 2.7
        bike_subtypes.append(["Light 2.7", "Light 2.x"])
        return bike_subtypes


get_public_data = helpers.singleton(MobikePublicData)

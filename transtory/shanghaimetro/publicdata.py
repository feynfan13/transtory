from transtory.common import singleton


class ShmPublicData(object):
    """Public data, including
        -- Lines
        -- Stations
        -- Trains
    """
    def __init__(self):
        pass

    def _make_train_type_and_range_list(self):
        # TODO: train type query system is too complicated
        #    the current method is to ask user to provide train type for new trains
        pass


get_public_data = singleton(ShmPublicData)


class ShmPublicDataApps(object):
    def __init__(self):
        self.public_data: ShmPublicData = get_public_data()

    def query_train_types(self):
        # TODO: check above
        pass

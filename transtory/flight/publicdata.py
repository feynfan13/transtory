from transtory.common import singleton


class FlightPublicDataApp(object):
    def __init__(self):
        pass


get_public_data_app = singleton(FlightPublicDataApp)
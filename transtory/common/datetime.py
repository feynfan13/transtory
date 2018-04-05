from datetime import datetime, timedelta, time
from pytz import timezone
from .infrastructure import singleton


class CityTimeZoneMap(object):
    city_to_time_zone = {
        "Shanghai": timezone("Asia/Shanghai"),
        "Tai'an": timezone("Asia/Shanghai"),
        "Los Angeles": timezone("America/Los_Angeles"),
        "San José": timezone("America/Los_Angeles"),
        "San Francisco": timezone("America/Los_Angeles"),
        "Denver": timezone("America/Denver"),
        "London": timezone("Europe/London"),
        "Helsinki": timezone("Europe/Helsinki"),
        "Tallahassee": timezone("America/New_York"),
        "Atlanta": timezone("America/New_York"),
        "Orlando": timezone("America/New_York")
    }

    def get_time_zone_of_city(self, city):
        return self.city_to_time_zone[city]


get_city_time_zone_map = singleton(CityTimeZoneMap)


class DateTimeHelper(object):
    """Wrapper for operations on date and time
    """
    date_str_format = "%Y-%m-%d"
    time_str_format = "%H:%M"
    # Use ISO8601 format
    datetime_str_format = date_str_format + " " + time_str_format
    time_stamp_format = "%Y%m%d%H%M%S"

    def __init__(self, date_zero=None):
        if date_zero is not None:
            self.date_zero = datetime.strptime(date_zero, self.date_str_format)

    @staticmethod
    def is_valid_date_str(date_str):
        if not date_str[0:4].isdigit():
            return False
        if not (date_str[5:7].isdigit() and int(date_str[5:7]) <= 12):
            return False
        if not (date_str[8:].isdigit() and int(date_str[8:]) <= 31):
            return False
        return True

    @staticmethod
    def is_valid_time_str(time_str):
        if not (time_str[0:2].isdigit() and int(time_str[0:1]) < 24):
            return False
        if not (time_str[3:].isdigit() and int(time_str[3:] < 60)):
            return False
        return True

    def get_date_str(self, date_obj):
        return date_obj.strftime(self.date_str_format)

    def get_date_from_str(self, date_str):
        return datetime.strptime(date_str, self.date_str_format)

    def get_current_date_str(self):
        return self.get_date_str(datetime.today())

    @staticmethod
    def plus_days(date, n):
        return date + timedelta(days=n)

    def get_datetime_compact_str(self, time_stamp):
        return time_stamp.strftime(self.time_stamp_format)

    def get_datetime_str(self, adatetime: datetime):
        return adatetime.strftime(self.datetime_str_format)

    def get_current_datetime_str(self):
        return self.get_datetime_str(datetime.now())

    def get_date_int_from_date_str(self, date_str):
        assert(self.date_zero is not None)
        if self.is_valid_date_str(date_str):
            the_date = self.get_date_from_str(date_str)
            return (the_date - self.date_zero).days
        else:
            raise ValueError("DateTimeOps::get_date_int_expr: wrong date str.")

    def get_date_int(self, dt):
        assert(self.date_zero is not None)
        return (dt - self.date_zero).days

    def get_date_str_from_int_expr(self, int_date):
        assert(self.date_zero is not None)
        date0 = self.plus_days(self.date_zero, int_date)
        return date0.strftime(self.date_str_format)

    def get_time_int_from_time_str(self, time_str):
        if self.is_valid_time_str(time_str):
            return int(time_str[0:2]) * 60 + int(time_str[3:])
        else:
            raise ValueError("DateTimeOps::get_time_int_expr: wrong date str.")

    @staticmethod
    def get_time_int(dt: datetime):
        return dt.hour * 60 + dt.minute

    @staticmethod
    def get_time_str_from_time_int(atime):
        hours, minutes = divmod(atime, 60)
        return "{:02d}:{:02d}".format(hours, minutes)

    @staticmethod
    def get_time_from_str(time_str):
        hour, minute = time_str.split(":")
        return time(int(hour), int(minute))

    def get_time_str(self, atime: time):
        return atime.strftime(self.time_str_format)

    @staticmethod
    def get_datetime_from_date_time(adate, atime: time):
        return datetime(adate.year, adate.month, adate.day, atime.hour, atime.minute)

    @staticmethod
    def get_datetime_from_str(datetime_str):
        date_str, time_str = datetime_str.split()
        year, month, day = [int(x) for x in date_str.split("-")]
        hour, min = [int(x) for x in time_str.split(":")]
        return datetime(year, month, day, hour, min, tzinfo=None)

    @staticmethod
    def get_time_zone_of_city(city):
        return get_city_time_zone_map().get_time_zone_of_city(city)

    def get_utc_datetime(self, datetime_obj: datetime, city):
        datetime_obj.replace(tzinfo=None)
        tz = self.get_time_zone_of_city(city)
        return tz.localize(datetime_obj).astimezone(timezone("UTC"))


class DateTimeWrapper(object):
    """Wrapper for operations on date and time
    """
    date_str_format = "%Y-%m-%d"
    time_str_format = "%H:%M"
    # Use ISO8601 format
    datetime_str_format = date_str_format + " " + time_str_format
    time_stamp_format = "%Y%m%d%H%M%S"

    def __init__(self):
        pass

    @staticmethod
    def is_valid_date_str(date_str):
        if not date_str[0:4].isdigit():
            return False
        if not (date_str[5:7].isdigit() and int(date_str[5:7]) <= 12):
            return False
        if not (date_str[8:].isdigit() and int(date_str[8:]) <= 31):
            return False
        return True

    @staticmethod
    def is_valid_time_str(time_str):
        if not (time_str[0:2].isdigit() and int(time_str[0:1]) < 24):
            return False
        if not (time_str[3:].isdigit() and int(time_str[3:] < 60)):
            return False
        return True

    def get_date_str(self, date_obj):
        return date_obj.strftime(self.date_str_format)

    def get_date_from_str(self, date_str):
        return datetime.strptime(date_str, self.date_str_format)

    def get_current_date_str(self):
        return self.get_date_str(datetime.today())

    @staticmethod
    def plus_days(date, n):
        return date + timedelta(days=n)

    def get_datetime_compact_str(self, time_stamp):
        return time_stamp.strftime(self.time_stamp_format)

    def get_datetime_str(self, adatetime: datetime):
        return adatetime.strftime(self.datetime_str_format)

    def get_current_datetime_str(self):
        return self.get_datetime_str(datetime.now())

    def get_date_int_from_date_str(self, date_str):
        assert(self.date_zero is not None)
        if self.is_valid_date_str(date_str):
            the_date = self.get_date_from_str(date_str)
            return (the_date - self.date_zero).days
        else:
            raise ValueError("DateTimeOps::get_date_int_expr: wrong date str.")

    def get_date_int(self, dt):
        assert(self.date_zero is not None)
        return (dt - self.date_zero).days

    def get_date_str_from_int_expr(self, int_date):
        assert(self.date_zero is not None)
        date0 = self.plus_days(self.date_zero, int_date)
        return date0.strftime(self.date_str_format)

    def get_time_int_from_time_str(self, time_str):
        if self.is_valid_time_str(time_str):
            return int(time_str[0:2]) * 60 + int(time_str[3:])
        else:
            raise ValueError("DateTimeOps::get_time_int_expr: wrong date str.")

    @staticmethod
    def get_time_int(dt: datetime):
        return dt.hour * 60 + dt.minute

    @staticmethod
    def get_time_str_from_time_int(atime):
        hours, minutes = divmod(atime, 60)
        return "{:02d}:{:02d}".format(hours, minutes)

    @staticmethod
    def get_time_from_str(time_str):
        hour, minute = time_str.split(":")
        return time(int(hour), int(minute))

    def get_time_str(self, atime: time):
        return atime.strftime(self.time_str_format)

    @staticmethod
    def get_datetime_from_date_time(adate, atime: time):
        return datetime(adate.year, adate.month, adate.day, atime.hour, atime.minute)

    @staticmethod
    def get_datetime_from_str(datetime_str):
        date_str, time_str = datetime_str.split()
        year, month, day = [int(x) for x in date_str.split("-")]
        hour, min = [int(x) for x in time_str.split(":")]
        return datetime(year, month, day, hour, min, tzinfo=None)

    @staticmethod
    def get_time_zone_of_city(city):
        return get_city_time_zone_map().get_time_zone_of_city(city)

    def get_utc_datetime(self, datetime_obj: datetime, city):
        datetime_obj.replace(tzinfo=None)
        tz = self.get_time_zone_of_city(city)
        return tz.localize(datetime_obj).astimezone(timezone("UTC"))

    def get_local_datetime_str_from_utc_datetime_str(self, dt_str, city):
        atz = self.get_time_zone_of_city(city)
        adt = self.get_datetime_from_str(dt_str)
        adt = adt.replace(tzinfo=timezone("UTC"))
        local_datetime = adt.astimezone(atz)
        return self.get_datetime_str(local_datetime)


dt_wrapper: DateTimeWrapper = singleton(DateTimeWrapper)()

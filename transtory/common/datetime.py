import datetime


class DateTimeHelper(object):
    """Wrapper for operations on date and time
    """
    date_str_format = "%Y-%m-%d"
    time_str_format = "%H:%M"
    datetime_str_format = date_str_format + " " + time_str_format
    time_stamp_format = "%Y%m%d%H%M%S"

    def __init__(self, date_zero=None):
        if date_zero is not None:
            self.date_zero = datetime.datetime.strptime(date_zero, self.date_str_format)

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
        return datetime.datetime.strptime(date_str, self.date_str_format)

    def get_current_date_str(self):
        return self.get_date_str(datetime.datetime.today())

    @staticmethod
    def plus_days(date, n):
        return date + datetime.timedelta(days=n)

    def get_datetime_str(self, time_stamp):
        return time_stamp.strftime(self.time_stamp_format)

    def get_current_datetime_str(self):
        return self.get_datetime_str(datetime.datetime.now())

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
    def get_time_str_from_time_int(time):
        hours, minutes = divmod(time, 60)
        return "{:02d}:{:02d}".format(hours, minutes)

    def get_time_str(self, time: datetime.time):
        return time.strftime(self.time_str_format)

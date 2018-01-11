import logging
from datetime import datetime

# Set the style of logging
transtory_logger = logging.getLogger("transtory")
transtory_logger.setLevel(logging.DEBUG)
fh = logging.FileHandler("transtory.log")
fh.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)


class LoggingMsecFormatter(logging.Formatter):
    converter = datetime.fromtimestamp

    def formatTime(self, record, datefmt=None):
        ct = self.converter(record.created)
        if datefmt:
            s = ct.strftime(datefmt)
        else:
            t = ct.strftime("%Y-%m-%d %H:%M:%S")
            s = "%s.%03d" % (t, record.msecs)
        return s


formatter = LoggingMsecFormatter("%(asctime)s [%(levelname)s] (%(filename)s line:%(lineno)d)  %(message)s")
fh.setFormatter(formatter)
ch.setFormatter(formatter)
transtory_logger.addHandler(fh)
transtory_logger.addHandler(ch)

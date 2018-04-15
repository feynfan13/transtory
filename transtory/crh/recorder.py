import os
import shutil
import glob
import jsmin
import json

from transtory.common import DateTimeHelper, FileSystemHelper

from .configs import get_configs, CrhSysConfigs
from .configs import get_datetime_helper
from .dbops import get_db_ops, CrhDbOps
from .dbops import InputTripEntry, InputRouteEntry, InputTicketEntry


class CrhRecorder(object):
    def __init__(self):
        self.configs: CrhSysConfigs = get_configs()
        self.db_ops: CrhDbOps = get_db_ops()
        self.dt_helper: DateTimeHelper = get_datetime_helper()
        self.fs_helper = FileSystemHelper()

    @staticmethod
    def _assign_none_fields(val):
        if val is None or len(val) == 0:
            return None
        return val

    @staticmethod
    def _make_datetime_str_from_log_data(log_date, log_time):
        date_str = "-".join([log_date[0:4], log_date[4:6], log_date[6:]])
        time_str = ":".join([log_time[0:2], log_time[2:]])
        return date_str + " " + time_str

    def _get_trains_from_train_str(self, train_str: str):
        if "&" in train_str:
            train0, train1 = train_str.split("&")
            if "[J]" in train0:
                train_str.replace("[J]", "")
                train_join = train0.strip().replace("[J]", "")
                train_seat = train1.strip()
                join_type = 2
            elif "[J]" in train1:
                train_seat = train0.strip()
                train_join = train1.strip().replace("[J]", "")
                join_type = 3
            else:
                raise ValueError("Invalid train string in log file {:s}".format(train_str))
        else:
            train_seat, train_join, join_type = train_str.strip(), None, None
        return train_seat, train_join, join_type

    def _make_input_trip_entry(self, log_struct):
        trip_entry = InputTripEntry()
        assert (log_struct['Version'] == 1)
        trip_entry.task = log_struct["Task"]
        trip_entry.train_num = log_struct["Train Number"]
        trip_entry.train_num_start = log_struct["Origin"]
        trip_entry.train_num_final = log_struct["Terminal"]
        trip_entry.note = log_struct["Note"]
        trip_entry.tickets = list()
        for ticket in log_struct['Tickets']:
            trip_entry.tickets.append(self._make_input_ticket_entry(ticket))
        trip_entry.routes = list()
        for route in log_struct['Segments']:
            trip_entry.routes.append(self._make_input_route_entry(route))
        return trip_entry

    def _make_input_ticket_entry(self, log_struct):
        ticket_entry = InputTicketEntry()
        ticket_entry.ticket_type = log_struct['Ticket type']
        ticket_entry.ticket_short_sn = log_struct['Ticket Number']
        ticket_entry.ticket_long_sn = log_struct['Ticket SN']
        ticket_entry.ticket_sold_by = log_struct['Ticket Sold By']
        ticket_entry.ticket_sold_type = log_struct['Ticket Sold Type']
        ticket_entry.price = log_struct['Ticket Price']
        ticket_entry.seat_type = log_struct['Seat Type']
        ticket_entry.seat_num = log_struct['Seat Number']
        ticket_entry.start = log_struct['Ticket start']
        ticket_entry.end = log_struct['Ticket end']
        ticket_entry.note = log_struct['Note']
        return ticket_entry

    def _make_input_route_entry(self, log_struct):
        route_entry = InputRouteEntry()
        train_return = self._get_trains_from_train_str(log_struct["Train"])
        route_entry.seat_train, route_entry.join_train, route_entry.join_type = train_return
        route_entry.carriage = log_struct["Carriage"]
        route_entry.note = log_struct["Note"]
        route_entry.start = log_struct["From"]
        route_entry.start_time = self._make_datetime_str_from_log_data(log_struct["From Date"],
                                                                       log_struct["From Time"])
        route_entry.start_time_schedule = self._make_datetime_str_from_log_data(log_struct["From Date"],
                                                                                log_struct["From Time Schedule"])
        route_entry.start_gate = log_struct["From Gate"]
        route_entry.start_platform = log_struct["From Platform"]
        route_entry.start_note = log_struct["From Note"]
        route_entry.final = log_struct["To"]
        route_entry.final_time = self._make_datetime_str_from_log_data(log_struct["To Date"],
                                                                       log_struct["To Time"])
        route_entry.final_time_schedule = self._make_datetime_str_from_log_data(log_struct["To Date"],
                                                                                log_struct["To Time Schedule"])
        route_entry.final_gate = log_struct["To Gate"]
        route_entry.final_platform = log_struct["To Platform"]
        route_entry.final_note = log_struct["To Note"]

        return route_entry

    def record_trips_from_json(self):
        fname_pattern = os.sep.join([self.configs.log_folder, "*.json"])
        log_files = [fname for fname in glob.glob(fname_pattern) if "template" not in fname]
        log_archive = self.configs.log_archive_folder
        for log_file in log_files:
            with open(log_file, encoding="utf8") as fin:
                log_struct = json.loads(jsmin.jsmin(fin.read()))
                trip_entry = self._make_input_trip_entry(log_struct)
                file_processed = self.db_ops.add_trip(trip_entry)
            if file_processed:
                fname = self.fs_helper.get_file_name(log_file)
                dst_fpath = os.sep.join([log_archive, fname])
                shutil.move(log_file, dst_fpath)


    def update_trips_from_xmls(self):
        # TODO: add update functionality for shanghaimetro recorder
        pass
import os
import glob
import json
import jsmin
import shutil

from transtory.common import FileSystemHelper

from .configs import FlightSysConfigs, get_configs
from .dbops import FlightDbOps, get_db_ops
from .dbops import DateTimeHelper, get_datetime_helper
from .dbops import InputTripEntry, InputRouteEntry, InputLegEntry


class FlightRecorder(object):
    def __init__(self):
        self.configs: FlightSysConfigs = get_configs()
        self.db_ops: FlightDbOps = get_db_ops()
        self.dt_helper: DateTimeHelper = get_datetime_helper()
        self.fs_helper = FileSystemHelper()

    @staticmethod
    def _change_input_time_str(time_str):
        return time_str[0:10] + " " + time_str[11:13] + ":" + time_str[13:15]

    def _make_input_leg_entry(self, log_struct):
        leg_entry = InputLegEntry()
        leg_entry.leg_seq = log_struct["Leg Number"]
        leg_entry.leg_type = log_struct["Leg Type"]
        leg_entry.start_airport = log_struct["From"]
        leg_entry.start_terminal = log_struct["From Terminal"]
        leg_entry.start_concourse = log_struct["From Concourse"]
        leg_entry.start_gate = log_struct["From Gate"]
        leg_entry.takeoff_runway = log_struct["Takeoff Runway"]
        leg_entry.pushback_time_FA = self._change_input_time_str(log_struct["FA Pushback Actual"])
        leg_entry.pushback_time_planned_FA = self._change_input_time_str(log_struct["FA Pushback Plan"])
        leg_entry.takeoff_time_FA = self._change_input_time_str(log_struct["FA Takeoff Actual"])
        leg_entry.takeoff_time_planned_FA = self._change_input_time_str(log_struct["FA Takeoff Plan"])
        leg_entry.departure_time_FR24 = self._change_input_time_str(log_struct["FR24 Departure Actual"])
        leg_entry.departure_time_planned_FR24 = self._change_input_time_str(log_struct["FR24 Departure Plan"])
        leg_entry.final_airport = log_struct["To"]
        leg_entry.final_terminal = log_struct["To Terminal"]
        leg_entry.final_concourse = log_struct["To Concourse"]
        leg_entry.final_gate = log_struct["To Gate"]
        leg_entry.landing_runway = log_struct["Landing Runway"]
        leg_entry.landing_time_FA = self._change_input_time_str(log_struct["FA Landing Actual"])
        leg_entry.landing_time_planned_FA = self._change_input_time_str(log_struct["FA Landing Plan"])
        leg_entry.gate_arrival_time_FA = self._change_input_time_str(log_struct["FA Gate Arrival Actual"])
        leg_entry.gate_arrival_time_planned_FA = self._change_input_time_str(log_struct["FA Gate Arrival Plan"])
        leg_entry.arrival_time_FR24 = self._change_input_time_str(log_struct["FR24 Landing"])
        leg_entry.arrival_time_planned_FR24 = self._change_input_time_str(log_struct["FR24 Arrival Plan"])
        return leg_entry

    def _make_input_segment_entry(self, log_struct):
        segment_entry = InputRouteEntry()
        segment_entry.segment_seq = log_struct["Segment Number"]
        segment_entry.segment_type = log_struct["Segment Type"]
        segment_entry.status = log_struct["Status"]
        segment_entry.flight = log_struct["Flight Number"]
        segment_entry.cabin = log_struct["Cabin"]
        segment_entry.seat = log_struct["Seat"]
        segment_entry.fare_code = log_struct["Fare Code"]
        segment_entry.boarding_group = log_struct["Boarding Group"]
        segment_entry.plane = log_struct["Plane"]
        segment_entry.plane_model = log_struct["Plane Type"]
        segment_entry.miles_from_FA = log_struct["FA Miles Flown"]
        legs = []
        for leg_struct in log_struct["Legs"]:
            legs.append(self._make_input_leg_entry(leg_struct))
        segment_entry.legs = legs
        return segment_entry

    def _make_input_trip_entry(self, log_struct):
        trip_entry = InputTripEntry()
        trip_entry.confirmation_num = log_struct["Confirmation Number"]
        trip_entry.e_ticket_num = log_struct["eTicket Number"]
        trip_entry.price = log_struct["Price"]
        segments = []
        for segment_struct in log_struct["Segments"]:
            segments.append(self._make_input_segment_entry(segment_struct))
        trip_entry.segments = segments
        return trip_entry

    def record_trips_from_json(self, is_commit=True):
        fname_pattern = os.sep.join([self.configs.log_folder, "*.json"])
        log_files = [fname for fname in glob.glob(fname_pattern) if "template" not in fname]
        log_archive = self.configs.log_archive_folder
        for log_file in log_files:
            with open(log_file, encoding="utf8") as fin:
                log_struct = json.loads(jsmin.jsmin(fin.read()))
                trip_entry = self._make_input_trip_entry(log_struct)
                trip_orm, trip_done = self.db_ops.get_or_add_trip(trip_entry, is_commit)
            if trip_done and is_commit:  # Move file if all segments are processed
                fname = self.fs_helper.get_file_name(log_file)
                dst_fpath = os.sep.join([log_archive, fname])
                shutil.move(log_file, dst_fpath)

    def update_trips_from_json(self):
        # TODO: add update functionality for flight recorder
        pass
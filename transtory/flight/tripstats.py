import os
import time

from .configs import FlightSysConfigs, get_configs
from .configs import logger

from .dbdefs import Trip, Route, Departure, Arrival, Airport, Airline
from .dbdefs import Plane, PlaneType

from .dbops import FlightDbOps, get_db_ops


class FlightTripStats(object):
    def __init__(self):
        pass
        self.configs: FlightSysConfigs = get_configs()
        self.save_folder = self.configs.stats_folder
        self.dbops: FlightDbOps = get_db_ops()
        self.session = self.dbops.session
        self.route_fields = ["reservation", "flight", "from", "pushback", "to", "gate_arrival", "plane", "type"]

    def _get_stats_full_path(self, fname):
        return os.path.sep.join([self.save_folder, fname])

    @staticmethod
    def _write_lists_to_csv(fout, val_list):
        """Goal of the function is to handle the None values properly
        """
        for val in val_list:
            if val is None:
                fout.write("||\t")
            elif isinstance(val, int):
                fout.write("|{:d}|\t".format(val))
            elif isinstance(val, str):
                fout.write("|{:s}|\t".format(val))
            else:
                raise Exception("Unsupported data type in csv writer: ", type(val))

    def _yield_route_list_entries(self):
        query = self.session.query(Trip, Route).join(Trip.routes)
        for trip, route in query.all():
            results = list()
            results.append(trip.confirmation_number)
            flight_number = self.dbops.get_flight_num(route.flight)
            results.append(flight_number)
            departure, arrival = route.departure, route.arrival
            airport0, airport1 = departure.airport, arrival.airport
            pushback, gate_arrival = departure.pushback_time, arrival.gate_arrival_time
            assert(pushback is not None and len(pushback) != 0)
            assert(gate_arrival is not None and len(gate_arrival) != 0)
            pushback = self.dbops.get_local_time_from_db_time(pushback, airport0.city)
            gate_arrival = self.dbops.get_local_time_from_db_time(gate_arrival, airport1.city)
            results.append(airport0.iata)
            results.append(pushback)
            results.append(airport1.iata)
            results.append(gate_arrival)
            results.append(route.plane.tail_number)
            # TODO: after plane_type table is built up, change this
            results.append(route.plane.type)
            # results.append(route.plane.type.name)
            yield results

    def save_route_list_csv(self):
        logger.info("Begin saving all routes.")
        start_time = time.clock()
        with open(self._get_stats_full_path("routes.csv"), "w", encoding="utf16") as fout:
            [fout.write("|{:s}|\t".format(x)) for x in self.route_fields]
            fout.write("\n")
            for result in self._yield_route_list_entries():
                self._write_lists_to_csv(fout, result)
                fout.write("\n")
        logger.info("Finished saving all routes (time used is {:f}s)".format(time.clock()-start_time))

    def save_all_stats(self):
        self.save_route_list_csv()

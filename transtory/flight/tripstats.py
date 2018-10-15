import os
import time

from .configs import FlightSysConfigs, get_configs
from .configs import logger

from .dbdefs import Trip, Route, Leg, Departure, Arrival, Airport, Airline
from .dbdefs import Plane, PlaneModel

from .dbops import FlightDbOps, get_db_ops


class FlightTripStats(object):
    def __init__(self):
        pass
        self.configs: FlightSysConfigs = get_configs()
        self.save_folder = self.configs.stats_folder
        self.dbops: FlightDbOps = get_db_ops()
        self.session = self.dbops.session
        self.route_fields = ['seq', 'reservation', 'flight', 'from', 'pushback', 'takeoff',
                             'to', 'landing', 'gate_arrival', 'plane', 'type']

    def _get_stats_full_path(self, fname):
        return os.path.sep.join([self.save_folder, fname])

    @staticmethod
    def _write_lists_to_csv(fout, val_list):
        """Goal of the function is to handle the None values properly
        """
        for val in val_list:
            if val is None:
                fout.write("||,")
            elif isinstance(val, int):
                fout.write("{:d},".format(val))
            elif isinstance(val, str):
                fout.write("|{:s}|,".format(val))
            else:
                raise Exception("Unsupported data type in csv writer: ", type(val))

    def _yield_route_list_entries(self):
        query = self.session.query(Trip, Route, Leg, Departure).join(Trip.routes).join(Route.legs)
        query = query.join(Leg.departure).order_by(Departure.pushback_time)
        for trip, route, leg, departure in query.all():
            results = list()
            results.append(trip.confirmation_number)
            flight_number = self.dbops.get_flight_num(route.flight)
            results.append(flight_number)
            departure, arrival = leg.departure, leg.arrival
            airport0, airport1 = departure.airport, arrival.airport
            pushback, gate_arrival = departure.pushback_time, arrival.gate_arrival_time
            takeoff, landing = departure.takeoff_time, arrival.landing_time
            if pushback is not None and len(pushback) != 0:
                pushback = self.dbops.get_local_time_from_db_time(pushback, airport0.city)
            else:
                pushback = 'NA'
            if gate_arrival is not None and len(gate_arrival) != 0:
                gate_arrival = self.dbops.get_local_time_from_db_time(gate_arrival, airport1.city)
            else:
                gate_arrival = 'NA'
            if takeoff is not None and len(takeoff) != 0:
                takeoff = self.dbops.get_local_time_from_db_time(takeoff, airport0.city)
            else:
                takeoff = 'NA'
            if landing is not None and len(landing) != 0:
                landing = self.dbops.get_local_time_from_db_time(landing, airport1.city)
            else:
                landing = 'NA'
            results.append(airport0.iata)
            results.append(pushback)
            results.append(takeoff)
            results.append(airport1.iata)
            results.append(landing)
            results.append(gate_arrival)
            results.append(route.plane.tail_number)
            # TODO: after plane_type table is built up, change this
            results.append(route.plane.model.name)
            # results.append(route.plane.type.name)
            yield results

    def save_route_list_csv(self):
        logger.info("Begin saving all routes.")
        start_time = time.clock()
        with open(self._get_stats_full_path("routes.csv"), 'w', encoding="utf8") as fout:
            fout.write('\ufeff')
            [fout.write('{:s},'.format(x)) for x in self.route_fields]
            fout.write("\n")
            for idx, result in enumerate(self._yield_route_list_entries()):
                fout.write('{:d},'.format(idx+1))
                self._write_lists_to_csv(fout, result)
                fout.write('\n')
        logger.info("Finished saving all routes (time used is {:f}s)".format(time.clock()-start_time))

    def save_all_stats(self):
        self.save_route_list_csv()

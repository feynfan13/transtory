import os
import time

from .configs import CrhSysConfigs, get_configs
from .configs import logger

from .dbdefs import Task, Trip, Route, Departure, Arrival, Station, Line, Ticket
from .dbdefs import Train, TrainService, TrainType

from .dbops import CrhDbOps, get_db_ops


class CrhTripStats(object):
    def __init__(self):
        self.configs: CrhSysConfigs = get_configs()
        self.save_folder = self.configs.stats_folder
        self.dbops: CrhDbOps = get_db_ops()
        self.session = self.dbops.session
        self.route_fields = ['seq', "task", "train_number", "from", "from_time", "to", "to_time", "trainset", "note",
                             'ticket', "seat_type", "seat", "from_gate", "from_platform", "to_platform", "to_gate",
                             "from_time_plan", "to_time_plan", "from_note", "to_note", "train_origin", "train_final",
                             "price", "ticket_short_sn", "ticket_long_sn", "ticket_sold_by", "ticket_sold_type"]

    def _get_stats_full_path(self, fname):
        return os.path.sep.join([self.save_folder, fname])

    @staticmethod
    def _empty_str_for_none(astr):
        return '??' if astr is None else astr

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
                raise Exception("Unsupported data type in csv writer.")

    def _yield_route_list_entries(self):
        query = self.session.query(Task, Trip, Route).join(Task.trips).join(Trip.routes).join()
        for task, trip, route in query.all():
            results = list()
            results.append(task.content)
            # TODO: we should consider adding a null object for each object table, including line
            if trip.line is not None:
                results.append(trip.line.name)
            else:
                results.append("")
            results.append(route.departure.station.chn_name)
            results.append(route.departure.time)
            results.append(route.arrival.station.chn_name)
            results.append(route.arrival.time)
            # Train service
            train_services = route.train_services
            if len(train_services) == 0:
                trainset_str = ""
            elif len(train_services) == 1:
                train_service = train_services[0]
                trainset_str = train_service.train.sn
            elif len(train_services) == 2:
                ts0, ts1 = train_services
                if ts1.operation_type == 0:
                    ts0, ts1 = ts1, ts0
                if ts1.operation_type == 1:
                    trainset_str = "{:s} & [J]{:s}".format(ts0.train.sn, ts1.train.sn)
                elif ts1.operation_type == 2:
                    trainset_str = "[J]{:s} & {:s}->".format(ts1.train.sn, ts0.train.sn)
                elif ts1.operation_type == 3:
                    trainset_str = "{:s} & [J]{:s}->".format(ts0.train.sn, ts1.train.sn)
                else:
                    raise Exception("Invalid train service operation type.")
            else:
                raise Exception("More than 2 train service entry for one route.")
            results.append(trainset_str)
            results.append(route.note)
            # Ticket part I
            ticket_seg = trip.tickets[0].start.station.chn_name
            seat_type, seat_number = '', ''
            for ticket in trip.tickets:
                ticket_seg += ('-'+ticket.end.station.chn_name)
                seat_type += (self._empty_str_for_none(ticket.seat_type) + '; ')
                seat_number += (self._empty_str_for_none(ticket.seat_number) + '; ')
            results.append(ticket_seg)
            results.append(seat_type[0:-2])
            results.append(seat_number[0:-2])
            # Departure & arrival
            results.append(route.departure.gate)
            results.append(route.departure.platform)
            results.append(route.arrival.platform)
            results.append(route.arrival.gate)
            results.append(route.departure.planned_time)
            results.append(route.arrival.planned_time)
            results.append(route.departure.note)
            results.append(route.arrival.note)
            if trip.line is None:
                results.append(None)
                results.append(None)
            else:
                results.append(trip.line.start.station.chn_name)
                results.append(trip.line.final.station.chn_name)
            # Ticket part II
            short_sn, long_sn, sold_by, sold_type, price = '', '', '', '', ''
            for ticket in trip.tickets:
                price += (self._empty_str_for_none(ticket.price) + '+')
                short_sn += (self._empty_str_for_none(ticket.short_sn) + '; ')
                long_sn += (self._empty_str_for_none(ticket.long_sn) + '; ')
                sold_by += (self._empty_str_for_none(ticket.sold_by) + '; ')
                sold_type += (self._empty_str_for_none(ticket.sold_type) + '; ')
            results.append(price[0:-1])
            results.append(short_sn[0:-2])
            results.append(long_sn[0:-2])
            results.append(sold_by[0:-2])
            results.append(sold_type[0:-2])
            yield results

    def save_route_list_csv(self):
        logger.info("Begin saving all routes.")
        start_time = time.perf_counter()
        with open(self._get_stats_full_path("routes.csv"), "w", encoding="utf8") as fout:
            fout.write('\ufeff')
            [fout.write("{:s},".format(x)) for x in self.route_fields]
            fout.write("\n")
            for idx, result in enumerate(self._yield_route_list_entries()):
                fout.write('{:d},'.format(idx+1))
                self._write_lists_to_csv(fout, result)
                fout.write("\n")
        logger.info("Finished saving all routes (time used is {:f}s)".format(time.perf_counter()-start_time))

    def save_all_stats(self):
        self.save_route_list_csv()

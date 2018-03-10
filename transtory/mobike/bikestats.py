import os
from sqlalchemy import func

from .dbops import MobikeDbOps, get_mobike_db_ops
from .dbops import DateTimeHelper, get_datetime_helper
from .dbops import MobikeSysConfigs, get_configs

from .dbdefs import Bike, BikeType, BikeSubtype
from .dbdefs import Trip, BikeService


class MobikeBikeStats(object):
    """Infrastructure for Mobike bike analysis
    The intention is to save various stats about bikes
    """
    def __init__(self):
        self.db_ops: MobikeDbOps = get_mobike_db_ops()
        self.dt_ops: DateTimeHelper = get_datetime_helper()
        self.configs: MobikeSysConfigs = get_configs()
        self.save_folder = self.configs.stats_folder
        self.session = self.db_ops.session

    def _get_stats_full_path(self, fname):
        return os.path.sep.join([self.save_folder, fname])

    def save_bike_list(self):
        query = self.session.query(Bike.sn, BikeSubtype.name, func.count(BikeService.id))
        query = query.join(Bike.services).join(Bike.subtype)
        query = query.group_by(Bike.sn).order_by(Bike.sn)
        with open(self._get_stats_full_path("bike.csv"), "w") as fout:
            fout.write("bike_sn,subtype,service_count\n")
            results = query.all()
            for bike in results:
                fout.write("|{:s}|,{:s},{:d}\n".format(bike[0], bike[1], bike[2]))

    def save_subtype_list(self):
        query = self.session.query(BikeSubtype.name, func.count(Bike.id))
        query = query.join(BikeSubtype.bikes)
        query = query.group_by(BikeSubtype.name).order_by(BikeSubtype.name)
        with open(self._get_stats_full_path("bike_subtype.csv"), "w") as fout:
            fout.write("subtype,bike_count\n")
            results = query.all()
            for subtype in results:
                fout.write("{:s},{:d}\n".format(subtype[0], subtype[1]))

    def save_type_list(self):
        query = self.session.query(BikeType.name, func.count(Bike.id))
        query = query.join(BikeType.subtypes).join(BikeSubtype.bikes)
        query = query.group_by(BikeType.name).order_by(BikeType.name)
        with open(self._get_stats_full_path("bike_type.csv"), "w") as fout:
            fout.write("type,bike_count\n")
            results = query.all()
            for bike_type in results:
                fout.write("{:s},{:d}\n".format(bike_type[0], bike_type[1]))

    def save_sn_segment_list(self):
        query_sn_seg = self.session.query(func.substr(Bike.sn, 1, 6).label("sn_seg")).group_by("sn_seg")
        with open(self._get_stats_full_path("bike_sn_segments.csv"), "w") as fout:
            fout.write("sn_segment,count,per_subtype")
            fout.write("\n")
            for sn_seg in query_sn_seg.all():
                sn_seg = sn_seg[0]
                query = self.session.query(BikeSubtype.id, func.count(Bike.id).label("count")).join(BikeSubtype.bikes)
                stmt = query.filter(Bike.sn.like(sn_seg+"%")).group_by(BikeSubtype.id).subquery()
                query = self.session.query(BikeSubtype.name, stmt.c.count).join(stmt, BikeSubtype.id == stmt.c.id)
                query = query.order_by(BikeSubtype.name)
                total_count, per_subtype_str = 0, ""
                for subtype_stat in query.all():
                    total_count += subtype_stat[1]
                    per_subtype_str += "{:s}({:d}),".format(subtype_stat[0], subtype_stat[1])
                fout.write("|{:s}|,{:d},{:s}".format(sn_seg, total_count, per_subtype_str))
                fout.write("\n")

    def save_bike_reuse_list(self):
        query = self.session.query(Bike).join(Bike.services).group_by(Bike.sn).order_by(Bike.sn)
        query = query.having(func.count(BikeService.id) > 1)
        with open(self._get_stats_full_path("bike_reuse.csv"), "w", encoding="utf8") as fout:
            fout.write('\ufeff')
            for bike_orm in query.all():
                fout.write("|{:s}|\t{:s}\n".format(bike_orm.sn, bike_orm.subtype.name))
                for service_orm in bike_orm.services:
                    trip_orm = service_orm.trip
                    fout.write("\t|{:s}|\t{:s}\t{:s}\n".format(trip_orm.time, trip_orm.departure_place,
                                                               trip_orm.arrival_place))

    def save_all_stats(self):
        self.save_bike_list()
        self.save_type_list()
        self.save_subtype_list()
        self.save_sn_segment_list()
        self.save_bike_reuse_list()

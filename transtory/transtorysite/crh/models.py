from django.db import models


class Task(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    content = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tasks'


class Station(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    chn_name = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'stations'


class TrainType(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    name = models.TextField(blank=True, null=True)
    code = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'train_types'


class Train(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    sn = models.TextField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    # type_id = models.IntegerField(blank=True, null=True)
    type = models.ForeignKey(TrainType, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'trains'


class LineStart(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    # station_id = models.IntegerField(blank=True, null=True)
    station = models.ForeignKey(Station, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'line_starts'


class LineFinal(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    # station_id = models.IntegerField(blank=True, null=True)
    station = models.ForeignKey(Station, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'line_finals'


class Line(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    name = models.TextField(blank=True, null=True)
    # line_start_id = models.IntegerField(blank=True, null=True)
    line_start = models.ForeignKey(LineStart, models.DO_NOTHING, blank=True, null=True)
    # line_final_id = models.IntegerField(blank=True, null=True)
    line_final = models.ForeignKey(LineFinal, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'lines'


class Ticket(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    short_sn = models.TextField(blank=True, null=True)
    long_sn = models.TextField(blank=True, null=True)
    sold_by = models.TextField(blank=True, null=True)
    sold_type = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tickets'


class Trip(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    # task_id = models.IntegerField(blank=True, null=True)
    task = models.ForeignKey(Task, models.DO_NOTHING, blank=True, null=True)
    # line_id = models.IntegerField(blank=True, null=True)
    line = models.ForeignKey(Line, models.DO_NOTHING, blank=True, null=True)
    seat_type = models.TextField(blank=True, null=True)
    seat_number = models.TextField(blank=True, null=True)
    price = models.TextField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    # ticket_id = models.IntegerField(blank=True, null=True)
    ticket = models.ForeignKey(Ticket, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'trips'


class Arrival(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    # station_id = models.IntegerField(blank=True, null=True)
    station = models.ForeignKey(Station, models.DO_NOTHING, blank=True, null=True)
    time = models.TextField(blank=True, null=True)
    planned_time = models.TextField(blank=True, null=True)
    gate = models.TextField(blank=True, null=True)
    platform = models.TextField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'arrivals'


class Departure(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    # station_id = models.IntegerField(blank=True, null=True)
    station = models.ForeignKey(Station, models.DO_NOTHING, blank=True, null=True)
    time = models.TextField(blank=True, null=True)
    planned_time = models.TextField(blank=True, null=True)
    gate = models.TextField(blank=True, null=True)
    platform = models.TextField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'departures'


class Route(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    # trip_id = models.IntegerField(blank=True, null=True)
    trip = models.ForeignKey(Trip, models.DO_NOTHING, blank=True, null=True)
    carriage = models.TextField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    # departure_id = models.IntegerField(blank=True, null=True)
    departure = models.ForeignKey(Departure, models.DO_NOTHING, blank=True, null=True)
    # arrival_id = models.IntegerField(blank=True, null=True)
    arrival = models.ForeignKey(Arrival, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'routes'


class TrainServices(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    # route_id = models.IntegerField(blank=True, null=True)
    route = models.ForeignKey(Route, models.DO_NOTHING, blank=True, null=True)
    # train_id = models.IntegerField(blank=True, null=True)
    train = models.ForeignKey(Train, models.DO_NOTHING, blank=True, null=True)
    operation_type = models.IntegerField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'train_services'

from django.db import models


class Task(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    task = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tasks'


class TrainType(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    name = models.TextField(blank=True, null=True)
    maker = models.TextField(blank=True, null=True)
    display_name = models.TextField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'train_types'


class Line(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    name = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'lines'


class Station(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    sn = models.TextField(blank=True, null=True)
    chn_name = models.TextField(blank=True, null=True)
    eng_name = models.TextField(blank=True, null=True)
    # line_id = models.IntegerField(blank=True, null=True)
    line = models.ForeignKey(Line, models.DO_NOTHING, blank=True, null=True)
    distance = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'stations'


class Train(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    sn = models.TextField(blank=True, null=True)
    # line_id = models.IntegerField(blank=True, null=True)
    line = models.ForeignKey(Line, models.DO_NOTHING, blank=True, null=True)
    # train_type_id = models.IntegerField(blank=True, null=True)
    train_type = models.ForeignKey(TrainType, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'trains'


class Arrival(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    # station_id = models.IntegerField(blank=True, null=True)
    station = models.ForeignKey(Station, models.DO_NOTHING, blank=True, null=True)
    line = models.ForeignKey(Line, models.DO_NOTHING, blank=True, null=True)
    time = models.TextField(blank=True, null=True)
    # time_retire = models.TextField(blank=True, null=True)
    # route_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'arrivals'


class Departure(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    # station_id = models.IntegerField(blank=True, null=True)
    station = models.ForeignKey(Station, models.DO_NOTHING, blank=True, null=True)
    time = models.TextField(blank=True, null=True)
    # date_retire = models.TextField(blank=True, null=True)
    # time_retire = models.TextField(blank=True, null=True)
    # route_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'departures'


class Route(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    # task_id = models.IntegerField(blank=True, null=True)
    task = models.ForeignKey(Task, models.DO_NOTHING, blank=True, null=True)
    # seq_retire = models.IntegerField(blank=True, null=True)
    # train_id = models.IntegerField(blank=True, null=True)
    train = models.ForeignKey(Train, models.DO_NOTHING, blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    # departure_id = models.IntegerField(blank=True, null=True)
    departure = models.ForeignKey(Departure, models.DO_NOTHING, blank=True, null=True)
    # arrival_id = models.IntegerField(blank=True, null=True)
    arrival = models.ForeignKey(Arrival, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'routes'

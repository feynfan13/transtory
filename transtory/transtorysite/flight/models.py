from django.db import models


class Airline(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    name = models.TextField(blank=True, null=True)
    iata = models.TextField(blank=True, null=True)
    icao = models.TextField(blank=True, null=True)
    callsign = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'airlines'


class Airport(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    iata = models.TextField(blank=True, null=True)
    icao = models.TextField(blank=True, null=True)
    city = models.TextField(blank=True, null=True)
    name = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'airports'


class PlaneModel(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    name = models.TextField(blank=True, null=True)
    maker = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'plane_models'


class Plane(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    tail_number = models.TextField(blank=True, null=True)
    msn = models.TextField(blank=True, null=True)
    # airline_id = models.IntegerField(blank=True, null=True)
    airline = models.ForeignKey(Airline, models.DO_NOTHING, blank=True, null=True)
    # type = models.TextField(blank=True, null=True)
    nickname = models.TextField(blank=True, null=True)
    # model_id = models.IntegerField(blank=True, null=True)
    model = models.ForeignKey(PlaneModel, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'planes'


class FlightFinal(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    # flight_id_retired = models.IntegerField(blank=True, null=True)
    # airport_id = models.IntegerField(blank=True, null=True)
    airport = models.ForeignKey(Airport, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'flight_finals'


class FlightStart(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    # flight_id_retired = models.IntegerField(blank=True, null=True)
    # airport_id = models.IntegerField(blank=True, null=True)
    airport = models.ForeignKey(Airport, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'flight_starts'


class Flight(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    number = models.TextField(blank=True, null=True)
    airline_id = models.IntegerField(blank=True, null=True)
    # start_id = models.IntegerField(blank=True, null=True)
    start = models.ForeignKey(FlightStart, models.DO_NOTHING, blank=True, null=True)
    # final_id = models.IntegerField(blank=True, null=True)
    final = models.ForeignKey(FlightFinal, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'flights'


class Trip(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    confirmation_number = models.TextField(blank=True, null=True)
    ticket_number = models.TextField(blank=True, null=True)
    price = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'trips'


class Arrival(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    # route_id_retired = models.IntegerField(blank=True, null=True)
    type = models.IntegerField(blank=True, null=True)
    # airport_id = models.IntegerField(blank=True, null=True)
    airport = models.ForeignKey(Airport, models.DO_NOTHING, blank=True, null=True)
    runway = models.TextField(blank=True, null=True)
    landing_time = models.TextField(blank=True, null=True)
    planned_landing_time = models.TextField(blank=True, null=True)
    terminal = models.TextField(blank=True, null=True)
    concourse = models.TextField(blank=True, null=True)
    gate = models.TextField(blank=True, null=True)
    gate_arrival_time = models.TextField(blank=True, null=True)
    planned_gate_arrival_time = models.TextField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'arrivals'


class Departure(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    # route_id_retired = models.IntegerField(blank=True, null=True)
    type = models.TextField(blank=True, null=True)
    pushback_time = models.TextField(blank=True, null=True)
    planned_pushback_time = models.TextField(blank=True, null=True)
    takeoff_time = models.TextField(blank=True, null=True)
    planned_takeoff_time = models.TextField(blank=True, null=True)
    # airport_id = models.IntegerField(blank=True, null=True)
    airport = models.ForeignKey(Airport, models.DO_NOTHING, blank=True, null=True)
    terminal = models.TextField(blank=True, null=True)
    concourse = models.TextField(blank=True, null=True)
    gate = models.TextField(blank=True, null=True)
    runway = models.TextField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'departures'


class Route(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    # trip_id = models.IntegerField(blank=True, null=True)
    trip = models.ForeignKey(Trip, models.DO_NOTHING, blank=True, null=True)
    seq = models.IntegerField(blank=True, null=True)
    type = models.IntegerField(blank=True, null=True)
    # plane_id = models.IntegerField(blank=True, null=True)
    plane = models.ForeignKey(Plane, models.DO_NOTHING, blank=True, null=True)
    # flight_id = models.IntegerField(blank=True, null=True)
    flight = models.ForeignKey(Flight, models.DO_NOTHING, blank=True, null=True)
    cabin = models.TextField(blank=True, null=True)
    seat = models.TextField(blank=True, null=True)
    fare_code = models.TextField(blank=True, null=True)
    boarding_group = models.TextField(blank=True, null=True)
    distance_fa = models.TextField(db_column='distance_FA', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'routes'


class Leg(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    # route_id = models.IntegerField(blank=True, null=True)
    route = models.ForeignKey(Route, models.DO_NOTHING, blank=True, null=True)
    # departure_id = models.IntegerField(blank=True, null=True)
    departure = models.ForeignKey(Departure, models.DO_NOTHING, blank=True, null=True)
    # arrival_id = models.IntegerField(blank=True, null=True)
    arrival = models.ForeignKey(Arrival, models.DO_NOTHING, blank=True, null=True)
    type = models.IntegerField(blank=True, null=True)
    seq = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'legs'




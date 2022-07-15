class InvalidTimeError(Exception):
    def __init__(self):
        super().__init__('Incorrect time')


class InvalidIntervalError(Exception):
    def __init__(self):
        super().__init__('Interval must be positive')


class InvalidLineNumberError(Exception):
    def __init__(self):
        super().__init__('Line number must be positive')


class TramNetwork():
    """
    Class TramNetwork. Contains attributes:
    :param list_tram_stops: all tram stops belonging to the network
    :type list_tram_stops: list

    :param list_lines: all tram lines belonging to the network
    :type list_lines: list
    """

    def __init__(self, list_tram_stops=None, list_lines=None):
        if list_tram_stops is None:
            self._list_tram_stops = []
        else:
            self._list_tram_stops = list_tram_stops
        if list_lines is None:
            self._list_lines = []
        else:
            self._list_lines = list_lines

    def get_list_tram_stops(self):
        return self._list_tram_stops

    def get_list_lines(self):
        return self._list_lines

    def get_name_tram_stops(self):
        return self._name_tram_stops

    def add_line(self, line):
        """
        Adds tram line to the tram network
        """
        self._list_lines.append(line)

    def get_distance(self, tram_stopA, tram_stopB):
        """
        Returns the time in which the tram travels between connected tram stops
        """
        for tram_stop in tram_stopA.get_connected_stops():
            if tram_stop[0] == tram_stopB:
                return tram_stop[1]


class TramLine():
    """
    Class TramLine. Contains attributes:
    :param name: a number that functions as a line name
    :type name: str

    :param list_tram_stops: all tram stops belonging to the line
    :type list_tram_stops: list

    :param hours_start, minutes_start: time of departure of the first tram
    :type hours_start, minutes_start: int

    :param interval: minutes between the departures of subsequent trams
                    (tram departs alternately from the beginning/end of line)
    :type interval: int

    :param list_trams: all trams belonging to the line
    :type list_trams: list
    """
    def __init__(
            self, name, list_trams_stops=None, hours_start=0,
            minutes_start=0, interval=15, list_trams=None):
        self._name = name
        if list_trams_stops is None:
            self._list_tram_stops = []
        else:
            self._list_tram_stops = list_trams_stops
        if list_trams is None:
            self._list_trams = []
        else:
            self._list_trams = list_trams
        self._moving_tram = []
        if hours_start < 0 or hours_start > 23:
            raise InvalidTimeError
        else:
            self._hours_start = hours_start
        if minutes_start < 0 or minutes_start > 59:
            raise InvalidTimeError
        else:
            self._minutes_start = minutes_start
        if interval <= 0:
            raise InvalidIntervalError
        else:
            self._interval = interval

    def get_number(self):
        return self._name

    def get_hours_start(self):
        return self._hours_start

    def get_minutes_start(self):
        return self._minutes_start

    def get_interval(self):
        return self._interval

    def get_list_tram(self):
        return self._list_trams

    def get_moving_tram(self):
        return self._moving_tram

    def get_itinerary(self):
        return self._list_tram_stops

    def add_tram(self, tram, number):
        """
        Adds tram to the tram line
        """
        self.get_list_tram().append((tram, number))


class TramStop():
    """
    Class TramStop. Contains attributes:
    :param name: tram stop's ID
    :type name: int

    :param x, y: the coordinates of the location of the tram stop
    :type x, y: int, int

    :param connected_stops_id: all ID's of connected tram stops with this
    :type connected_stops_id: list of int

    :param connected_stops: minutes_start: all connected tram stops with this
    :type connected_stops: list of objects
    """
    def __init__(
                self, id, name, x=0, y=0,
                connected_stops_id=None, connected_stops=None):
        self._id = id
        self._x = x
        self._y = y
        self._name = name
        if connected_stops_id is None:
            self._connected_stops_id = []
        else:
            self._connected_stops_id = connected_stops_id
        if connected_stops is None:
            self._connected_stops = []
        else:
            self._connected_stops = connected_stops

    def get_id(self):
        return self._id

    def set_id(self, id):
        self._id = id

    def get_name(self):
        return self._name

    def get_x(self):
        return self._x

    def get_y(self):
        return self._y

    def set_x(self, x):
        self._x = x

    def set_y(self, y):
        self._y = y

    def get_connected_stops(self):
        return self._connected_stops

    def add_connected_stop(self, other, distance):
        """
        Adds pair of connected tram stops
        """
        self._connected_stops.append((other, distance))
        other._connected_stops.append((self, distance))


class Tram():
    """
    Class Tram. Contains attributes:
    :param line: the tram line on which this tram runs
    :type line: TramLine

    :param line_number: number in what order this tram belong to the line
    :type line_number: int

    :param x, y: the coordinates of the actual location of the tram
    :type x, y: int, int
    """
    def __init__(self, line, line_number, x=0, y=0):
        self._line = line
        if line_number <= 0:
            raise InvalidLineNumberError
        else:
            self._line_number = line_number
        line.add_tram(self, line_number)
        self._x = x
        self._y = y
        self._last_tram_stop_number = 0
        self._activated = False
        last_line_number = self.get_line_number()-1
        self._tram_interval = last_line_number * self._line.get_interval()
        self._itinerary = []
        self._last_tram_stop = 0
        self._move = False

    def get_point(self):
        return self._point

    def get_line(self):
        return self._line

    def set_line(self, line):
        self._line = line

    def get_line_number(self):
        return self._line_number

    def set_line_number(self, line_number):
        self._line_number = line_number

    def get_tram_name(self):
        return self.get_line().get_number()

    def add_to_line(self, line, number):
        """
        Adds tram to the tram line
        """
        line.add_tram(self, number)
        self.set_line(line)
        self.set_line_number(number)

    def get_x(self):
        return self._x

    def set_x(self, x):
        self._x = x

    def get_y(self):
        return self._y

    def set_y(self, y):
        self._y = y

    def get_last_tram_stop_number(self):
        return self._last_tram_stop_number

    def get_last_tram_stop(self):
        return self._last_tram_stop

    def increase_last_tram_stop_number(self):
        self._last_tram_stop_number += 1

    def get_activated(self):
        return self._activated

    def set_activated(self, value):
        self._activated = value

    def get_start_time(self):
        """
        Returns the starting time of this tram converted into minutes
        """
        tram_line = self.get_line()
        minutes = tram_line.get_minutes_start()
        hours = tram_line.get_hours_start()*60
        time_to_start = minutes + hours
        return time_to_start + self._tram_interval

    def restart_start_time(self):
        self._tram_interval = 0
        tram_line = self.get_line()
        itinerary = tram_line.get_itinerary()
        if self.get_line_number() % 2 == 0:
            self.itinerary = itinerary[::-1]
        else:
            self.itinerary = itinerary

    def increase_tram_interval(self):
        """
        Increases the tram start time so that tram could repeats its itinerary
        """
        tram_line = self.get_line()
        quantity_of_tram = len(tram_line.get_list_tram())
        self._tram_interval += quantity_of_tram*tram_line.get_interval()

    def set_itinerary(self, itinerary):
        if self.get_line_number() % 2 == 0:
            self.itinerary = itinerary[::-1]
        else:
            self.itinerary = itinerary

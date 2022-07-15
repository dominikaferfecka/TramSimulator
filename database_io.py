from database import TramLine, TramStop


class MalformedDataError(Exception):
    pass


class InvalidTramStopPositionError(Exception):
    pass


class ConnectionAlreadySetError(Exception):
    pass


def check_position(list_tram_stops, new_x, new_y):
    for tram_stop in list_tram_stops:
        x = tram_stop.get_x()
        y = tram_stop.get_y()
        if new_x == x and new_y == y:
            raise InvalidTramStopPositionError


def read_tram_stop(file_handle):
    """
    Gets basic data about tram stops from configuration file.
    Adds tram stops to tram network database.
    """
    try:
        list_tram_stops = []
        for line in file_handle:
            line = line.rstrip()
            tokens = line.split(',')
            id, name, x, y = tokens
            check_position(list_tram_stops, int(x), int(y))
            tram_stop = TramStop(id, name, int(x), int(y))
            list_tram_stops.append(tram_stop)
        return list_tram_stops
    except ValueError:
        raise MalformedDataError


def check_connection(tram_stopA, tram_stopB):
    for tram_stop_tuple in tram_stopB.get_connected_stops():
        tram_stop, distance = tram_stop_tuple
        if tram_stop == tram_stopA:
            raise ConnectionAlreadySetError


def read_tram_stop_connection(file_handle, network):
    """
    Gets basic data about connection between tram stops.
    Adds connection between tram stops to tram network database.
    """
    try:
        for line in file_handle:
            line = line.rstrip()
            tokens = line.split(',')
            tram_stopA_id, tram_stopB_id, time_between = tokens
            for tram_stop in network.get_list_tram_stops():
                if tram_stopA_id == tram_stop.get_id():
                    tram_stopA = tram_stop
                if tram_stopB_id == tram_stop.get_id():
                    tram_stopB = tram_stop
            check_connection(tram_stopA, tram_stopB)
            tram_stopA.add_connected_stop(tram_stopB, int(time_between))
    except ValueError:
        raise MalformedDataError


def read_tram_line(file_handle, network):
    """
    Gets basic data about tram lines from configuration file.
    Adds tram lines to tram network database.
    """
    try:
        tram_line_list = []
        for line in file_handle:
            line = line.rstrip()
            tokens = line.split(',')
            tram_stops_id_list = []
            tram_stop_list = []
            line_number = tokens[0]
            hours_start = int(tokens[1])
            minutes_start = int(tokens[2])
            interval = int(tokens[3])
            for element in tokens[4:]:
                tram_stops_id_list.append(element)
            for tram_stop_id in tram_stops_id_list:
                for tram_stop in network.get_list_tram_stops():
                    if tram_stop_id == tram_stop.get_id():
                        tram_stop_list.append(tram_stop)
            tram_line = TramLine(
                                line_number, tram_stop_list,
                                hours_start, minutes_start, interval)
            tram_line_list.append(tram_line)
        return tram_line_list
    except IndexError:
        raise MalformedDataError

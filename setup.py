import argparse
from database import TramNetwork, Tram
from database_io import (
    read_tram_stop,
    read_tram_stop_connection,
    read_tram_line
)


class TramPathNotFoundError(Exception):
    pass


class TramPermissionError(Exception):
    pass


class TramPathCannotBeDirectory(Exception):
    pass


def network_setup(args):
    """
    Paths to configuration files.
    Opens configuration files.
    Creates trams - five trams for each line
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--file-tramstop')
    parser.add_argument('--file-connection')
    parser.add_argument('--file-tramline')
    arguments = parser.parse_args(args[1::])
    if arguments.file_tramstop:
        path_tram_stop = arguments.file_tramstop
    else:
        path_tram_stop = 'tram_stops.txt'
    if arguments.file_connection:
        path_tram_stop_connection = arguments.file_connection
    else:
        path_tram_stop_connection = 'tram_stops_connection.txt'
    if arguments.file_tramline:
        path_tram_line = arguments.file_tramline
    else:
        path_tram_line = 'tram_line.txt'

    try:
        with open(path_tram_stop, 'r') as file_handle:
            list_tram_stops = read_tram_stop(file_handle)
        network = TramNetwork(list_tram_stops)
        with open(path_tram_stop_connection, 'r') as file_handle:
            read_tram_stop_connection(file_handle, network)
        with open(path_tram_line, 'r') as file_handle:
            list_tram_line = read_tram_line(file_handle, network)
    except FileNotFoundError:
        raise TramPathNotFoundError
    except PermissionError:
        raise TramPermissionError
    except IsADirectoryError:
        raise TramPathCannotBeDirectory

    for tram_line in list_tram_line:
        for tram_number_line in range(1, 6):
            Tram(tram_line, tram_number_line)
        network.add_line(tram_line)

    return network

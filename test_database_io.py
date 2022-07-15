from database_io import (
                            read_tram_line,
                            read_tram_stop_connection,
                            read_tram_stop,
                            MalformedDataError,
                            InvalidTramStopPositionError,
                            ConnectionAlreadySetError)
from database import TramNetwork, TramStop, InvalidTimeError
from io import StringIO
import pytest

"""
Unit tests to test getting data from configuration files
and creation of tram network database
"""


def test_read_tram_stop():
    data = '1,Teatr Bagatela,20,-70\n2,Stary Kleparz,80,-110'
    file_handle = StringIO(data)
    list_tram_stops = read_tram_stop(file_handle)
    assert list_tram_stops[0].get_name() == "Teatr Bagatela"
    assert list_tram_stops[1].get_id() == '2'


def test_read_tram_stop_position():
    data = '1,Teatr Bagatela,20,-70\n2,Stary Kleparz,80,-110'
    file_handle = StringIO(data)
    list_tram_stops = read_tram_stop(file_handle)
    assert list_tram_stops[0].get_x() == 20
    assert list_tram_stops[1].get_y() == -110


def test_read_tram_stop_invalid_position():
    data = '1,Teatr Bagatela,0,0\n2,Stary Kleparz,0,0'
    file_handle = StringIO(data)
    with pytest.raises(InvalidTramStopPositionError):
        read_tram_stop(file_handle)


def test_read_tram_stop_invalid():
    data = '1,Teatr Bagatela,20\n2,Stary Kleparz,80,-110'
    file_handle = StringIO(data)
    with pytest.raises(MalformedDataError):
        read_tram_stop(file_handle)


def test_read_tram_stop_connection():
    data = '1,2,4\n1,3,5'
    file_handle = StringIO(data)
    tram_stopA = TramStop('1', 'Teatr Bagatela')
    tram_stopB = TramStop('2', 'Stary Kleparz')
    tram_stopC = TramStop('3', 'Teatr Słowackiego')
    list_tram_stops = [tram_stopA, tram_stopB, tram_stopC]
    network = TramNetwork(list_tram_stops)
    read_tram_stop_connection(file_handle, network)
    tram_list = [(tram_stopB, 4), (tram_stopC, 5)]
    assert tram_stopA.get_connected_stops() == tram_list


def test_read_tram_stop_connection_invalid():
    data = '1,2,4,5\n1,3,5'
    file_handle = StringIO(data)
    tram_stopA = TramStop('1', 'Teatr Bagatela')
    tram_stopB = TramStop('2', 'Stary Kleparz')
    tram_stopC = TramStop('3', 'Teatr Słowackiego')
    list_tram_stops = [tram_stopA, tram_stopB, tram_stopC]
    network = TramNetwork(list_tram_stops)
    with pytest.raises(MalformedDataError):
        read_tram_stop_connection(file_handle, network)


def test_read_tram_stop_connection_already_set():
    data = '1,2,4\n1,2,5'
    file_handle = StringIO(data)
    tram_stopA = TramStop('1', 'Teatr Bagatela')
    tram_stopB = TramStop('2', 'Stary Kleparz')
    list_tram_stops = [tram_stopA, tram_stopB]
    network = TramNetwork(list_tram_stops)
    with pytest.raises(ConnectionAlreadySetError):
        read_tram_stop_connection(file_handle, network)


def test_tram_line():
    data = '1,5,0,20,50,49,14,13,12,4,3\n2,5,30,15,50,49,14,13,1,2,3,8,9,18,19'
    file_handle = StringIO(data)
    tram_stopA = TramStop('1', 'Teatr Bagatela')
    tram_stopB = TramStop('2', 'Stary Kleparz')
    tram_stopC = TramStop('3', 'Teatr Słowackiego')
    list_tram_stops = [tram_stopA, tram_stopB, tram_stopC]
    network = TramNetwork(list_tram_stops)
    tram_line_list = read_tram_line(file_handle, network)
    assert len(tram_line_list) > 0


def test_tram_line_invalid_time():
    data = '1,5,60,20,50,49,14,13,12,4,3\n2,5,30,15,50,49,14,13,1,2,3,8,9,18'
    file_handle = StringIO(data)
    tram_stopA = TramStop('1', 'Teatr Bagatela')
    tram_stopB = TramStop('2', 'Stary Kleparz')
    tram_stopC = TramStop('3', 'Teatr Słowackiego')
    list_tram_stops = [tram_stopA, tram_stopB, tram_stopC]
    network = TramNetwork(list_tram_stops)
    with pytest.raises(InvalidTimeError):
        read_tram_line(file_handle, network)


def test_tram_line_invalid():
    data = '1,5,0\n2,5,30,15,50,49,14,13,1,2,3,8,9,18,19'
    file_handle = StringIO(data)
    tram_stopA = TramStop('1', 'Teatr Bagatela')
    tram_stopB = TramStop('2', 'Stary Kleparz')
    tram_stopC = TramStop('3', 'Teatr Słowackiego')
    list_tram_stops = [tram_stopA, tram_stopB, tram_stopC]
    network = TramNetwork(list_tram_stops)
    with pytest.raises(MalformedDataError):
        read_tram_line(file_handle, network)

from database import TramNetwork, TramLine, TramStop, Tram
from database import (
                InvalidTimeError,
                InvalidIntervalError,
                InvalidLineNumberError
                )
import pytest

"""
Unit tests to test the database of the tram network
"""


def test_create_tram_network_objects():
    tram_stopA = TramStop(1, 'Teatr Bagatela')
    tram_stopB = TramStop(2, 'Stary Kleparz')
    tram_stopC = TramStop(3, 'Teatr Słowackiego')
    list_tram = [tram_stopA, tram_stopB, tram_stopC]
    simulator = TramNetwork(list_tram)
    list_trams = simulator.get_list_tram_stops()
    assert list_trams == list_tram


def test_connected_tram_stops():
    tram_stopA = TramStop(1, 'Teatr Bagatela')
    tram_stopB = TramStop(2, 'Stary Kleparz')
    tram_stopC = TramStop(3, 'Teatr Słowackiego')
    list_tram = [tram_stopA, tram_stopB, tram_stopC]
    TramNetwork(list_tram)
    tram_stopA.add_connected_stop(tram_stopB, 4)
    tram_stopB.add_connected_stop(tram_stopC, 3)
    connected_tram_stopB = tram_stopB.get_connected_stops()
    assert connected_tram_stopB == [(tram_stopA, 4), (tram_stopC, 3)]


def test_tram_stops_distance():
    tram_stopA = TramStop(1, 'Teatr Bagatela')
    tram_stopB = TramStop(2, 'Stary Kleparz')
    tram_stopC = TramStop(3, 'Teatr Słowackiego')
    list_tram = [tram_stopA, tram_stopB, tram_stopC]
    simulator = TramNetwork(list_tram)
    tram_stopA.add_connected_stop(tram_stopB, 4)
    tram_stopB.add_connected_stop(tram_stopC, 3)
    distance = simulator.get_distance(tram_stopA, tram_stopB)
    assert distance == 4


def test_create_tram_line():
    tram_stopA = TramStop(1, 'Teatr Bagatela')
    tram_stopB = TramStop(2, 'Stary Kleparz')
    tram_stopC = TramStop(3, 'Teatr Słowackiego')
    list_tram_stops = [tram_stopA, tram_stopB, tram_stopC]
    TramNetwork(list_tram_stops)
    tram_stopA.add_connected_stop(tram_stopB, 4)
    tram_stopB.add_connected_stop(tram_stopC, 3)
    tram_line4 = TramLine(4, list_tram_stops)
    assert tram_line4.get_number() == 4
    assert tram_line4.get_itinerary() == list_tram_stops


def test_create_add_tram():
    tram_stopA = TramStop(1, 'Teatr Bagatela')
    tram_stopB = TramStop(2, 'Stary Kleparz')
    tram_stopC = TramStop(3, 'Teatr Słowackiego')
    list_tram_stops = [tram_stopA, tram_stopB, tram_stopC]
    TramNetwork(list_tram_stops)
    tram_stopA.add_connected_stop(tram_stopB, 4)
    tram_stopB.add_connected_stop(tram_stopC, 3)
    tram_line4 = TramLine(4, list_tram_stops)
    tram = Tram(tram_line4, 1)
    tram_list = tram_line4.get_list_tram()
    assert tram_list == [(tram, 1)]
    line = tram.get_line()
    assert line == tram_line4


def test_create_tram_line_invalid_time_hours():
    tram_stopA = TramStop(1, 'Teatr Bagatela')
    tram_stopB = TramStop(2, 'Stary Kleparz')
    tram_stopC = TramStop(3, 'Teatr Słowackiego')
    list_tram_stops = [tram_stopA, tram_stopB, tram_stopC]
    TramNetwork(list_tram_stops)
    tram_stopA.add_connected_stop(tram_stopB, 4)
    tram_stopB.add_connected_stop(tram_stopC, 3)
    with pytest.raises(InvalidTimeError):
        TramLine(4, list_tram_stops, 24, 00)


def test_create_tram_line_invalid_time_minutes():
    tram_stopA = TramStop(1, 'Teatr Bagatela')
    tram_stopB = TramStop(2, 'Stary Kleparz')
    tram_stopC = TramStop(3, 'Teatr Słowackiego')
    list_tram_stops = [tram_stopA, tram_stopB, tram_stopC]
    TramNetwork(list_tram_stops)
    tram_stopA.add_connected_stop(tram_stopB, 4)
    tram_stopB.add_connected_stop(tram_stopC, 3)
    with pytest.raises(InvalidTimeError):
        TramLine(4, list_tram_stops, 5, 60)


def test_create_tram_line_invalid_interval():
    tram_stopA = TramStop(1, 'Teatr Bagatela')
    tram_stopB = TramStop(2, 'Stary Kleparz')
    tram_stopC = TramStop(3, 'Teatr Słowackiego')
    list_tram_stops = [tram_stopA, tram_stopB, tram_stopC]
    TramNetwork(list_tram_stops)
    tram_stopA.add_connected_stop(tram_stopB, 4)
    tram_stopB.add_connected_stop(tram_stopC, 3)
    with pytest.raises(InvalidIntervalError):
        TramLine(4, list_tram_stops, 5, 5, -1)


def test_create_invalid_tram():
    tram_stopA = TramStop(1, 'Teatr Bagatela')
    tram_stopB = TramStop(2, 'Stary Kleparz')
    tram_stopC = TramStop(3, 'Teatr Słowackiego')
    list_tram_stops = [tram_stopA, tram_stopB, tram_stopC]
    TramNetwork(list_tram_stops)
    tram_stopA.add_connected_stop(tram_stopB, 4)
    tram_stopB.add_connected_stop(tram_stopC, 3)
    tram_line4 = TramLine(4, list_tram_stops)
    with pytest.raises(InvalidLineNumberError):
        Tram(tram_line4, -1)

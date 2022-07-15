from PySide2.QtWidgets import QApplication, QMainWindow
from ui_tram_simulator import Ui_MainWindow
from PySide2.QtWidgets import QGraphicsScene, QGraphicsSimpleTextItem
from PySide2.QtCore import QTimer, QPointF, Qt
from PySide2.QtGui import QBrush, QColor, QFont, QPainter
from setup import network_setup
import sys


class FatalError(Exception):
    def __init__(self):
        super().__init__('Fatal error, simulator cannot work')


class Clock():
    """
    Class Clock. Contains attributes:
    :param hours: responsible for keeping time: hours(0-23)
    :type hours: int

    :param minutes: responsible for keeping time: minutes(0-59)
    :type minutes: int
    """
    def __init__(self, hours=5, minutes=0, parent=None):
        super().__init__()
        self._hours = hours
        self._minutes = minutes

    def get_hours(self):
        return self._hours

    def increase_hours(self):
        if self._hours == 23:
            self._hours = 0
        else:
            self._hours += 1
        self._minutes = 0

    def get_minutes(self):
        return self._minutes

    def increase_minutes(self):
        self._minutes += 1

    def get_time_in_minutes(self):
        return self.get_minutes() + 60*self.get_hours()

    def increase_time(self):
        if self.get_minutes() == 59:
            self.increase_hours()
        else:
            self.increase_minutes()


class TramSimulatorWindow(QMainWindow):
    """
    Class TramSimulatorWindow. Contains attributes:
    :param network: main tram network
    :type network: TramNetwork

    :param clock: responsible for keeping time
    :type clock: Clock
    """
    def __init__(self, network, clock, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self._scene = QGraphicsScene()
        self.ui.TramStopMap.setScene(self._scene)
        self.ui.TramStopMap.setRenderHint(QPainter.Antialiasing)
        self.ui.TramStopMap.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self._network = network

        self.set_tram_stops()
        self.set_line_between_tram_stops()
        self.showMaximized()
        self.clock_setup(clock)

    def clock_setup(self, clock):
        hours = clock.get_hours()
        minutes = clock.get_minutes()
        self._old_time = self._scene.addText(f'{hours}:0{minutes}')
        self._old_time.setFont(QFont("Times New Roman", 14))
        self._old_time.setPos(850, -350)
        self._clock = clock

    def get_scene(self):
        return self._scene

    def set_tram_stops(self):
        """
        Sets all tram stops on the scene
        """
        scene = self.get_scene()
        for tram_stop in self._network.get_list_tram_stops():
            marker = scene.addEllipse(-5, -5, 10, 10)
            marker.setZValue(1)
            marker.setBrush(QBrush(QColor(150, 0, 200)))
            name = tram_stop.get_name()
            tram_stop_name = QGraphicsSimpleTextItem(name, marker)
            tram_stop_name.setFont(QFont("Times New Roman", 8))
            marker.setPos(tram_stop.get_x(), tram_stop.get_y())
            tram_stop_name.setPos(0, 7)

    def set_line_between_tram_stops(self):
        """
        Sets line between each connected tram stops on the scene
        """
        scene = self.get_scene()
        for tram_stop in self._network.get_list_tram_stops():
            if len(tram_stop.get_connected_stops()) > 0:
                for connected_tuple in tram_stop.get_connected_stops():
                    connected_tram_stop = connected_tuple[0]
                    from_x = tram_stop.get_x()
                    from_y = tram_stop.get_y()
                    to_x = connected_tram_stop.get_x()
                    to_y = connected_tram_stop.get_y()
                    line = scene.addLine(from_x, from_y, to_x, to_y)
                    line.setPos(0, 0)

    def set_tram(self):
        """
        Recognizes which tram should be placed on the scene
        """
        for tram_line in self._network.get_list_lines():
            itinerary = tram_line.get_itinerary()
            for tram_tuple in tram_line.get_list_tram():
                tram = tram_tuple[0]
                minutes = self._clock.get_minutes()
                hours = self._clock.get_hours()
                if minutes == 0 and hours == 4:
                    tram.restart_start_time()
                if self._clock.get_time_in_minutes() == tram.get_start_time():
                    tram.increase_tram_interval()
                    if tram._move is False:
                        self.create_tram(itinerary, tram, tram_line)
                    tram.set_activated(True)
                    tram._move = True

    def create_tram(self, itinerary, tram, tram_line):
        """
        Creates and sets trams on the scene
        """
        tram.set_itinerary(itinerary)
        first_tram_stop = tram.itinerary[0]
        marker, tram_name = self.create_marker(tram)
        x = first_tram_stop.get_x()
        y = first_tram_stop.get_y()
        marker.setPos(x, y)
        tram_name.setPos(-15, -20)
        tram_line._moving_tram.append((tram, marker, tram_name))
        tram.set_x(x)
        tram.set_y(y)

    def create_marker(self, tram):
        """
        Creates ellipse for tram and sets on the scene
        """
        marker = self.get_scene().addEllipse(-4, -4, 8, 8)
        marker.setBrush(QBrush(QColor(0, 0, 255)))
        marker.setZValue(1)
        tram_name = self.create_tram_name_point(tram, marker)
        return (marker, tram_name)

    def create_tram_name_point(self, tram, marker):
        tram_name = QGraphicsSimpleTextItem(tram.get_tram_name(), marker)
        tram_name.setFont(QFont("Times New Roman", 8))
        tram_name.setBrush(QBrush(QColor(255, 0, 0)))
        return tram_name

    def move_tram_in_tram_line(self):
        """
        Recognizes which tram should be moved
        """
        for tram_line in self._network.get_list_lines():
            for tram_tuple in tram_line.get_moving_tram():
                tram = tram_tuple[0]
                point = tram_tuple[1]
                tram_name_point = tram_tuple[2]
                if tram.get_activated() is True:
                    if not tram.get_last_tram_stop() == tram.itinerary[-1]:
                        self.move_tram(tram, tram_line, point, tram_name_point)
                    else:
                        """
                        Tram restart - when the tram reaches last tram stop,
                        it stops moving and its route is reversed
                        """
                        tram.set_activated(False)
                        tram.itinerary = tram.itinerary[::-1]
                        tram._last_tram_stop_number = 0

    def count_distance_move(self, next_tram_stop, last_tram_stop):
        distance = self._network.get_distance(last_tram_stop, next_tram_stop)
        x_difference = next_tram_stop.get_x() - last_tram_stop.get_x()
        move_x = float(x_difference)/distance
        y_difference = next_tram_stop.get_y() - last_tram_stop.get_y()
        move_y = float(y_difference)/distance
        return (move_x, move_y)

    def move_tram(self, tram, tram_line, point, tram_name_point):
        """
        Moves trams on the scene
        """
        last = tram.itinerary[tram.get_last_tram_stop_number()]
        next = tram.itinerary[tram.get_last_tram_stop_number()+1]
        move_x, move_y = self.count_distance_move(next, last)
        x = tram.get_x()
        y = tram.get_y()
        point.setPos(point.pos() + QPointF(move_x, move_y))
        tram.set_x(x+move_x)
        tram.set_y(y+move_y)
        if next.get_x() == tram.get_x():
            if next.get_y() == tram.get_y():
                tram._last_tram_stop = next
                tram.increase_last_tram_stop_number()

    def setup_tram(self):
        self.set_tram()
        self.move_tram_in_tram_line()

    def display_time(self):
        """
        Increases and displays the simulation time
        """
        if self._clock.get_minutes() <= 9:
            time = f'{self._clock.get_hours()}:0{self._clock.get_minutes()}'
        else:
            time = f'{self._clock.get_hours()}:{self._clock.get_minutes()}'
        self._scene.removeItem(self._old_time)
        new_time = self._scene.addText(time)
        new_time.setFont(QFont("Times New Roman", 14))
        new_time.setPos(850, -350)
        self._old_time = new_time
        self._clock.increase_time()


def guiMain(args):
    """
    Opens the simulation window.
    Counts the time in simulation
            (1000 ms in real time = 1 minute in simulation time)
    """
    try:
        network = network_setup(args)
        app = QApplication(args)
        clock = Clock()
        window = TramSimulatorWindow(network, clock)
        timer = QTimer()
        timer.setInterval(1000)
        timer.timeout.connect(window.setup_tram)
        timer.timeout.connect(window.display_time)
        timer.start()
        window.show()
        return app.exec_()
    except Exception:
        return FatalError


if __name__ == "__main__":
    guiMain(sys.argv)

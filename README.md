﻿# TramSimulator

The simulation shows a tram network consisting of numerous stops and tram lines.

Trams follow the route of the tram stops in the order in which they are assigned to the line. The departure time of the first tram is specified for each line, and subsequent trams depart at a set time interval. Trams with an odd assignment number will depart from the first stop, while those with an even number will depart from the last stop. After completing the route of the entire line, they stop and then cross it again in the opposite direction. 

The travel time between each pair of adjacent stops is constant. The project assumes no delays and tram collisions, and each track segment is bi-directional. The status of the tram network is refreshed every second, reflecting the minute during the simulation.

**Running simulation**

In order to run the simulation, enter the command by running the file responsible for the graphical user interface: python3 gui.py.
Additionally, you can specify the path to your own source files by entering optional commands:

• _--file-tramstop_
enters the path to the file containing data about tram stops

• _--file-connection_
enters the path to a file containing connection data between stops

• _--file-tramline_
enters the path to the file containing data about tram lines

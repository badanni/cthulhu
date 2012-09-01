#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       servidor_novo.py
#       
#       Copyright 2012 Danny Enrique Vasconez <dannyvasconeze@gmail.com>
#                      Daniel Engiberto Granda Guitierrez <degranda87@gmail.com>
#       
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.


from AriaPy import *
from ArNetworkingPy import *
import sys
"""\package servidor_novo
   \brief Servidor para el Pioneer P3-DX
   \details Se lo puede utilizar con multiples conexiones de clientes trabaja en el puerto 7272
   La lista de comandos para el paquete ArNetPacket se encuentra en el anexo 1
   \authors    Danny Vasconez
   \authors   Daniel Granda
   \version   0.0.2
   \date      2012
   \pre       Tener conectada la plataforma Pioneer P3-DX.
   \bug       Nada
   \warning   uso inapropiado puede hacer que la aplicacion falle
   
"""

def requestCallback(client, packet):
  """
  \brief Sirve cuando se manda el comando "test" en el paquete
  \param client El cliente que manda el paquete
  \param packet el paquete que recibe el servidor para el comando 
  \return Nada
  """
  replyPacket = ArNetPacket()
  replyPacket.strToBuf(str(robot.getPose().x));
  print "requestCallback received a packet with command #%d. Sending a reply...\n" % (packet.getCommand())
  client.sendPacketTcp(replyPacket)
def movimiento(client,packet):
  """
  \brief Sirve cuando se manda el comando "mover" en el paquete
  \param client El cliente que manda el paquete
  \param packet el paquete que recibe el servidor para el comando 
  \return Nada
  """
  robot.lock()
  robot.comInt(8,5000) #move(5000) para atras move(-4999)
  robot.unlock()
def rotar(client,packet):
  """
  \brief Sirve cuando se manda el comando "rotar" en el paquete
  \param client El cliente que manda el paquete
  \param packet el paquete que recibe el servidor para el comando 
  \return Nada
  """
  robot.lock()
  robot.comInt(12,50) 
  robot.unlock()
def posicion(client,packet):
  """
  \brief Sirve cuando se manda el comando "pose" en el paquete
  \param client El cliente que manda el paquete
  \param packet el paquete que recibe el servidor para el comando 
  \return ArNetPacket con la informacion en coordenadas X,Y,T al cliente
  """
  robot.lock()
  poses = sonarDev.getCurrentBufferAsVector()
  packet=ArNetPacket()
  packet.doubleToBuf(len(poses))
  for p in poses:
    print p
    valor=str(p).strip('(').strip(')').strip('X:')
    valor=valor.split(",")
    valor_x=valor[0]
    valor_y=valor[1].strip().strip('Y:')
    packet.byte4ToBuf(int(float(valor_x)))
    packet.byte4ToBuf(int(float(valor_y)))
  packet.finalizePacket()
  print packet.verifyCheckSum()
  client.sendPacketTcp(packet)
  robot.unlock()

# This example demonstrates how to use ArNetworking in Python. 

# Global library initialization, just like the C++ API:
Aria.init()

# Create a robot object:
robot = ArRobot()

# make a gyro 
gyro = ArAnalogGyro(robot)

#sonar, must be added to the robot
sonarDev = ArSonarDevice(7)
#add the sonar to the robot
robot.addRangeDevice(sonarDev)

# make the core server object:
server = ArServerBase()
#
packet = ArNetPacket()
#
#anadir comandos
server.addData("test", "move(30)", requestCallback, "none", "none")
server.addData("rotar", "move(30)", rotar, "none", "none")
server.addData("mover", "move30", movimiento, "none", "none")
server.addData("pose", "valores del sensor en X,Y,T", posicion, "none", "primero el numero de sensores y luego sus valores X,Y,T")
#
# Create a "simple connector" object and connect to either the simulator
# or the robot. Unlike the C++ API which takes int and char* pointers, 
# the Python constructor just takes argv as a list.
print "Connecting..."

con = ArSimpleConnector(sys.argv)
if (not con.connectRobot(robot)):
    print "Could not connect to robot, exiting"
    Aria.exit(1)

#
server.resetTracking()

#
# Open the server on port 7272:
if (not server.open(7272)):
    print "Could not open server, exiting"
    Aria.exit(1)

# Create various services and attach them to the core server
serverInfoRobot = ArServerInfoRobot(server, robot)
serverInfoSensor = ArServerInfoSensor(server, robot)
drawings = ArServerInfoDrawings(server)
drawings.addRobotsRangeDevices(robot)

# ways of moving the robot
modeStop = ArServerModeStop(server, robot)
modeRatioDrive = ArServerModeRatioDrive(server, robot)
modeWander = ArServerModeWander(server, robot)
modeStop.addAsDefaultMode()
modeStop.activate()

# set up the simple commands ("custom commands" in MobileEyes)
commands = ArServerHandlerCommands(server)
# add the simple commands for the microcontroller
uCCommands = ArServerSimpleComUC(commands, robot)
# add the simple commands for logging
loggingCommands = ArServerSimpleComMovementLogging(commands, robot)
# add the simple commands for the gyro
gyroCommands = ArServerSimpleComGyro(commands, robot, gyro)
# Add the simple command for logging the robot config and orig robot config
configCommands = ArServerSimpleComLogRobotConfig(commands, robot)
    
# Run the robot and server threads in the background:
print "Running..."
robot.runAsync(1)

server.runAsync()

robot.enableMotors()

robot.waitForRunExit()

#
#while (server.getRunningWithLock()):
#  ArUtil.sleep(1000)
#  server.broadcastPacketTcp(packet, "updateNumbers")
#


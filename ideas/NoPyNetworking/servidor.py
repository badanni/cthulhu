#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       untitled.py
#       
#       Copyright 2012 Danny E Vasconezz <badanni@badanni-Inspiron-N5110>
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
#       
#       

#Robot ARIA
from AriaPy import *
import sys


#Servidor
import socket

class NoPyArNetworking:
	def server(self):
		s = socket.socket()
		s.bind(("192.168.2.113", 9999))#"192.168.2.113"
		s.listen(2) #maximo de clientes
		sc, addr = s.accept()
		while True:
			recibido = sc.recv(1024)
			recibido=recibido.split(',')
			if recibido[0] == "quit":
				break
			if recibido[0] == "adelante":
				self.mover(1,0)
			if recibido[0] == "sonares":
				self.sonares()
			print "Recibido:", recibido
			sc.send(recibido[0])
		print "adios"
		sc.close()
		s.close()
		return 0

	def mover(self,direcion1,direcion2):
		# Drive the robot a bit, then exit.
		self.robot.lock()
		print "Robot position using ArRobot accessor methods: (", self.robot.getX(), ",", self.robot.getY(), ",", self.robot.getTh(), ")"
		pose = self.robot.getPose()
		print "Robot position by printing ArPose object: ", pose
		print "Robot position using special python-only ArPose members: (", pose.x, ",", pose.y, ",", pose.th, ")"
		print "Sending command to move forward 1 meter..."
		self.robot.enableMotors()
		self.robot.move(1000)
		self.robot.unlock()

	def sonares(self,numero_de_sonares=7):
		self.robot.lock()
		poses = self.sonarDev.getCurrentBufferAsVector()
		print "Sonar readings (%d) (Point coordinates in space):" % (len(poses))
		for p in poses:
			print "    sonar reading at ", p
		self.robot.unlock()

	def robot(self):
		# Global library initialization, just like the C++ API:
		Aria.init()

		# Create a robot object:
		self.robot = ArRobot()
		
		#gyro = ArAnalogGyro(self.robot)
		#sonar, must be added to the robot
		self.sonarDev = ArSonarDevice(7)
		#add the sonar to the robot
		self.robot.addRangeDevice(self.sonarDev)

		# Create a "simple connector" object and connect to either the simulator
		# or the robot. Unlike the C++ API which takes int and char* pointers, 
		# the Python constructor just takes argv as a list.
		print "Connecting..."

		con = ArSimpleConnector(sys.argv)
		if not con.parseArgs():
			con.logOptions()
			Aria.exit(1)

		if not con.connectRobot(self.robot):
			print "Could not connect to robot, exiting"
			Aria.exit(1)


		# Run the robot threads in the background:
		print "Running..."
		self.robot.runAsync(1)
		#self.robot.enableMotors()
		#robot.waitForRunExit()

if __name__ == '__main__':
	a=NoPyArNetworking()
	a.robot()
	a.server()


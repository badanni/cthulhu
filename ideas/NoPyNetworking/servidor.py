#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       servidor.py
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
#       
#       

#Robot ARIA
from AriaPy import *
import sys


#Servidor
import socket

"""\package servidor_NoPyArnetwoking
   \brief Servidor para el Pioneer P3-DX
   \details Se lo puede utilizar con un maximo de dos conexiones de clientes trabaja en el puerto especificado al ejecutarlo
   \authors    Danny Vasconez
   \authors   Daniel Granda
   \version   0.0.1
   \date      2012
   \pre       Tener conectada la plataforma Pioneer P3-DX.
   \bug       Si se cierra la conexion se tiene que volver a abrir el servidor.
   \warning   uso inapropiado puede hacer que la aplicacion falle
   
"""
"""
   \section intro Ejemplo de uso
   En el ejemplo se muestra como utilizar esta clase.
   \verbinclude ejemplo_servidor
"""
class NoPyArNetworking:
	"""
	\class Servidor.NoPyArNetworking
	\brief es la clase encargada del servidor 
	\details sirve para poder darle ordenes a la plataforma y obtener informacion de esta.
	"""
	def __init__(self):
		"""
		\brief crear las variables de sonares y odometria
		\param self no se lo utiliza es solo por pertener a la clase
		\return Nada
		"""
		self.valor_sonares={}
		self.valor_odometria="x,y,th"

	def server(self,ip,puerto):
		"""
		\brief Es el servidor ya que aqui se determina que segun los comandos recibidos que accion realizar
		\param self Este parametro no es necesario escribir, es como un puntero
		\param ip (\c str) El IP de la maquina donde se ejecuta el servidor
		\param puerto (\c int) El puerto donde se realizara la conexion
		\return 0
		"""
		s = socket.socket()
		s.bind((ip, puerto))#"192.168.2.113",9999
		s.listen(2) #maximo de clientes
		sc, addr = s.accept()
		while True:
			recibido = sc.recv(1024)
			recibido=recibido.split(',')
			if recibido[0] == "apagar":
				break
			elif recibido[0] == "adelante":
				self.mover(1,0,recibido[1])
			elif recibido[0] == "atras":
				self.mover(-1,0,recibido[1])
			elif recibido[0] == "izq":
				self.mover(0,-1,recibido[1])
			elif recibido[0] == "der":
				self.mover(0,1,recibido[1])
			elif recibido[0] == "odometria":
				self.odometria()
				sc.send(self.valor_odometria)
			elif recibido[0] == "sonares":
				self.sonares()
				sc.send(str(len(self.valor_sonares)))
				bandera1=None
				while bandera1!=str(len(self.valor_sonares)):
					bandera1=sc.recv(1024)
				for va in self.valor_sonares:
					sc.send(self.valor_sonares[va])
					bandera1=None
					while bandera1!="listo":
						bandera1=sc.recv(1024)
			print "Recibido:", recibido
			sc.send(recibido[0])
		print "adios"
		sc.close()
		s.close()
		return 0

	def odometria(self):
		"""
		\brief Es la orden que obtiene la informacion de odometria y estado de la baretia de la plataforma
		\param self Este parametro no es necesario escribir, es como un puntero
		"""
		print "Robot position using ArRobot accessor methods: (", self.robot.getX(), ",", self.robot.getY(), ",", self.robot.getTh(), ")"
		pose = self.robot.getPose()
		print "Robot position by printing ArPose object: ", pose
		print "Robot position using special python-only ArPose members: (", pose.x, ",", pose.y, ",", pose.th, ")"
		self.valor_odometria= str(pose.x)+","+str(pose.y)+","+str(pose.th)+","+str(self.robot.getRealBatteryVoltage())

	def mover(self,direcion1,direcion2,velocidad=1000):
		"""
		\brief Es la orden que realiza el movimiento y velocidad de la plataforma
		\param self Este parametro no es necesario escribir, es como un puntero
		\param direcion1 (\c int) Es un valor que puede ser 1 o -1. Uno para ir adelante y menos uno para ir atras
		\param direcion2 (\c int) Es un valor que puede ser 1 o -1. Uno para ir a la derecha y menos uno para ir a la izquierda
		\param velocidad (\c int) Es el valor que determina la velocidad de desplazamiento de la plataforma
		"""
		# Drive the robot a bit, then exit.
		if ((direcion1!=0) & (direcion2==0)):
			self.robot.lock()
			self.robot.setVel(float(velocidad))
			print "Sending command to move forward %d meter..." % (100*direcion1)
			print self.robot.getVel()
			self.robot.move(100*direcion1)
			self.robot.unlock()
		elif ((direcion1==0) & (direcion2!=0)):
			self.robot.lock()
			self.robot.setRotVel(int(velocidad))
			angulo=self.robot.getTh()+10*direcion2
			print "Sending command to rotate %d degrees..." % (angulo)
			print self.robot.getRotVel()
			print self.robot.getRotVelMax()
			self.robot.setHeading(angulo)
			self.robot.unlock()

	def sonares(self):
		"""
		\brief Es la orden que obtiene la informacion de los sonares
		\param self Este parametro no es necesario escribir, es como un puntero
		"""
		self.robot.lock()
		poses = self.sonarDev.getCurrentBufferAsVector()
		print "Sonar readings (%d) (Point coordinates in space):" % (len(poses))
		who=0
		for p in poses:
			print "    sonar reading at ", p
			valor=str(p).strip('(').strip(')').strip('X:')
			valor=valor.split(",")
			valor_x=valor[0]
			valor_y=valor[1].strip().strip('Y:')
			self.valor_sonares.update({'s%d' % (who):"%s , %s" % (valor_x,valor_y)})
			who+=1
			print valor_x, valor_y
		self.robot.unlock()

	def robot(self):
		"""
		\brief Es la orden que inicializa el robot y fija parametros basicos
		\param self Este parametro no es necesario escribir, es como un puntero
		"""
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
		self.robot.enableMotors()
		#disableSonar()
		#enableSonar()
		#getDirectMotionPrecedenceTime(self)
		print self.robot.getVel()
		print self.robot.getRotVel()
		#setVel()
		#setRotVel()
		#robot.waitForRunExit()
def mensaje():
	a="""No ingreso los parametros de ip y puerto por lo tanto se va a
usar localhost:9999 . Para ingresar los parametros corretamente 
correctamente se debe tipear en consola:
$ python servidor.py 192.168.1.115 9999
"""
	print a
if __name__ == '__main__':
	a=NoPyArNetworking()
	
	if len(sys.argv)==3:
		a.robot()
		a.server(sys.argv[1],int(sys.argv[2]))
	else:
		mensaje()
		a.robot()
		a.server("localhost",9991)


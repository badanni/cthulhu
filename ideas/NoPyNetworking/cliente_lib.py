#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  sin título.py
#  
#  Copyright 2012 DannyE <badanni@badanni-desktop>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  
import socket
from time import sleep
class cliente_lib:
	def __init__(self):
		self.sonar=[None,None,None,None,None,None,None]
		self.odometria=[None,None,None,None]
		self.ip="localhost"
		self.puerto=9991
	
	def conexion(self):
		self.s = socket.socket()
		self.s.connect((self.ip, self.puerto))

	def envio_movimiento(self,comando,para1=None,para2=None):
		self.s.send(comando)
		respuesta=self.s.recv(1024)
		self.respuesta=respuesta
		verificacion=self.s.recv(1024)

	def odometria_comando(self):
		self.s.send("odometria")
		odometria=self.s.recv(1024)
		self.odometria=odometria.split(",")
		verificacion=self.s.recv(1024)

	def sonares_comando(self):
		self.s.send("sonares")
		sonar=[None,None,None,None,None,None,None]
		cantidad=self.s.recv(1024)
		self.s.send(cantidad)
		for a in range(int(cantidad)):
			sonar[a]=self.s.recv(1024)
			self.s.send("listo")
		self.sonar=sonar
		verificacion=self.s.recv(1024)

	def cerrar_conexion(self):
		self.s.send("apagar")
		self.s.close()

def main():
	a=cliente_lib()
	#a.ip="192.168.2.105"
	#a.puerto=9999
	a.conexion()
	a.sonares_comando()
	print a.sonar
	a.odometria_comando()
	print a.odometria
	a.cerrar_conexion()
	return 0

if __name__ == '__main__':
	main()


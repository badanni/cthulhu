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
		self.x={}
		self.y={}
		self.ip="localhost"
		self.puerto=9999
	
	def conexion(self):
		self.s = socket.socket()
		self.s.connect((self.ip, self.puerto))

	def envio_movimiento(self,comando,para1=None,para2=None):
		if para1!=None:
			self.s.send(comando+","+para1)
		else:
			self.s.send(comando)
		respuesta=self.s.recv(1024)
		self.respuesta=respuesta

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
		verificacion=self.s.recv(1024) #suelta al servidor de su ciclo 
		bandera1=0
		acu=0
		#print sonar
		for i in range(2*int(cantidad)):
			valores=sonar[acu].split(",")
			#print valores
			if bandera1==0:
				self.x.update({'x%d' % (acu):valores[0]})
				bandera1=1
			else:
				self.y.update({'y%d' % (acu):valores[1]})
				bandera1=0
				acu=acu+1
			if acu==cantidad:
				acu=0

	def cerrar_conexion(self):
		self.s.send("apagar")
		self.s.close()

def main():
	a=cliente_lib()
	a.ip="192.168.2.105"
	a.puerto=9999
	a.conexion()
	a.sonares_comando()
	print a.sonar
	print a.x
	print a.y
	a.odometria_comando()
	print a.odometria
	a.cerrar_conexion()
	return 0

if __name__ == '__main__':
	main()


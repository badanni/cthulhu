#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       cliente.py terminal de pruebas
#       
#       Copyright 2012 Danny E Vasconez <dannyvasconeze@gmail.com>
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

# Cliente:
import socket


def main():
	s = socket.socket()
	#s.connect(("192.168.2.113", 9019))
	s.connect(("localhost", 9991))
	while True:
		mensaje = raw_input("> ")
		s.send(mensaje)
		if mensaje == "desconectar"
			print s.recv(1024)
			break
		if mensaje == "apagar":
			print "Adios"
			break
		elif mensaje == "odometria":
			odometria=s.recv(1024)
			odometria=odometria.split(",")
			print odometria
		elif mensaje == "sonares":
			sonar=[None,None,None,None,None,None,None]
			cantidad=s.recv(1024)
			s.send(cantidad)
			for a in range(int(cantidad)):
				sonar[a]=s.recv(1024)
				s.send("listo")
				print sonar[a]
		mensaje=s.recv(1024)
		print mensaje
	s.close()
	return 0

if __name__ == '__main__':
	main()


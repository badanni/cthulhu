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

#Servidor
import socket

def main():
	s = socket.socket()
	s.bind(("localhost", 9999))
	s.listen(2) #maximo de clientes
	sc, addr = s.accept()
	while True:
		recibido = sc.recv(1024)
		recibido=recibido.split(',')
		if recibido[0] == "quit":
			break
		print "Recibido:", recibido
		sc.send(recibido)
	print "adios"
	sc.close()
	s.close()
	return 0

if __name__ == '__main__':
	main()


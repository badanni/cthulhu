#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       sin título.py
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


import sys
import time
"""\package gamepad
   \brief libreria para leer el puerto del joystick o gamepad
   \details Tener conectada la palanca para funcionar
   \authors   Danny Vasconez
   \authors   Daniel Granda
   \version   0.0.1
   \date      2012
   \pre       Ninguno
   \bug       Ninguno
   \warning   Ninguno
   
"""
"""
   \section intro Ejemplo de uso
   En el ejemplo se muestra como utilizar esta libreria
   \verbinclude ejemplo_gamepadv1
"""

class gamepad:
	"""
	\class gamepad.gamepad
	\brief es la clase encargada de la palanca 
	\details  se lo utiliza para leer el flujo de datos de /dev/input/js0 para conocer el estados de los botones del gamepad
	"""
	def __init__(self):
		"""
		\brief Carga valores a las variables necesarias para funcionar la libreria
		\details  este comando no es necesario utilizarlo es usado al instanciar la clase
		\param self este parametro no es necesario escribir
		"""
		self.a=0

	def gamepad_init(self):
		"""
		\brief Sirve realizar el enlace con la direccion /dev/input/js0 que representa la palanca
		\details  Este comando es el que realizar la conexion con la palanca.
		\param self este parametro no es necesario escribir
		\return pipe, msg. La varible pipe es el enlace virtual con la palanca
		"""
		#Abre el dispositivo js0 como si fuera un archivo de lectura
		pipe=open('/dev/input/js0','r')
		msg=[]
		return pipe,msg
	def gamepad_lectura(self,pipe,msg):
		"""
		\brief Sirve leer los estados de la palanca
		\details  Este comando es el encargado de leer el flujo de datos y interpretarlos
		\param self este parametro no es necesario escribir
		\param pipe es el enlace virtual con la palanca
		\param msg es arreglo para almacenar los valores del flujo de datos de la palanca
		\return a 
		"""
		#time.sleep(5)
		a=0
		#Para cada caracter leidos desde el /dev/input/js0 pipe..
		for char in pipe.read(1):
			#Agrega la representacion entera de la lectura de caracteres Unicode en la lista msg.
			msg+=[ord(char)]
			#print len(msg)
			#Si el tamanio de la lista msg es 8
			if len(msg) == 8:
				#Boton evento si el byte 6 es 1
				if msg[6] == 1: #1
					if msg[4] == 0:
						if msg[7] == 0:
							#print "Boton 1"
							a='b1'
						elif msg[7] == 1:
							#print "Boton 2"
							a='b2'
						elif msg[7] == 2:
							#print "Boton 3"
							a='b3'
						elif msg[7] == 3:
							#print "Boton 4"
							a='b4'
						elif msg[7] == 4:
							#print "Boton L1"
							a='l1'
						elif msg[7] == 5:
							#print "Boton R1"
							a='r1'
						elif msg[7] == 6:
							#print "Boton L2"
							a='l2'
						elif msg[7] == 7:
							#print "Boton R2"
							a='r2'
				#ejes evento if el byte 6 es 2
				elif msg[6] == 2:
					if msg[5] == 128:
						if msg[7] == 1:
							#print "Boton Arriba"
							a='ar'
						elif msg[7] == 0:
							#print "Boton Izquierda"
							a='iz'
					elif msg[5] == 127:
						if msg[7] == 0:
							#print "Boton Derecha"
							a='de'
						elif msg[7] == 1:
							#print "Boton Abajo"
							a='ab'
				#resetear msg como una lista vacia
				msg[0:] = []
		self.a=a
		return a
if __name__ == '__main__':
	c=gamepad()
	pipe,msg=c.gamepad_init()
	while 1:
		a=c.gamepad_lectura(pipe,msg)
		if a!=0:
			print a
	#break


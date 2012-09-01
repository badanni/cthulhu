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
from AriaPy import *

class gamepad:
	def __init__(self):
		pass
	def iniciar(self):
		#Aria.init() #No es necesario para funcionar
		gamepad=ArJoyHandler()
		gamepad.init() #Inicializa el gamepad
		gamepad.setSpeeds(100, 700)
		key=ArKeyHandler()
		a=0
		b=0 #Botones
		d=0 #direcion
		print gamepad.getNumButtons(), "Numero de botones de la palanca"
		print gamepad.getNumAxes(), "Numero de ejes en la palanca"
		print "presione ESC para salir"
		while a!=260:
			a=key.getKey()
			#Botones de la palanca
			c=gamepad.getButton(1)
			c2=gamepad.getButton(2)
			c3=gamepad.getButton(3)
			c4=gamepad.getButton(4)
			r1=gamepad.getButton(5)
			l1=gamepad.getButton(6)
			r2=gamepad.getButton(7)
			l2=gamepad.getButton(8)
			eje1=gamepad.getAxis(1) #Izq- der
			eje2=gamepad.getAxis(2) #Arriba-abajo
			if (gamepad.haveJoystick()==True & c==True):
				if eje2!=0:
					if eje2==1:
						d="ar"
					else:
						d="ab"
				if eje1!=0:
					if eje1==1:
						d="de"
					else:
						d="iz"
				if c==False:
					b="b1" #presiono tecla 1
				elif c2==True:
					b="b2" #presiono tecla 2
				elif c3==True:
					b="b3" #presiono tecla 3
				elif c4==True:
					b="b4" #presiono tecla 4
				elif r1==True:
					b="r1" #presiono tecla R1
				elif r2==True:
					b="r2" #presiono tecla R2
				elif l1==True:
					b="l1" #presiono tecla L1
				elif l2==True:
					b="l2" #presiono tecla L2
		return d,b

if __name__ == '__main__':
	a=gamepad()
	print a.iniciar()


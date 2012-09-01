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
"""\package gamepad
   \brief libreria para leer el puerto del joystick o gamepad
   \details Se debe especificar el boton para el hombre muerto o este sera tomado como el boton 1
   \authors   Danny Vasconez
   \authors   Daniel Granda
   \version   0.0.2
   \date      2012
   \pre       Tener instalado la libreria AriaPy
   \bug       Ninguno
   \warning   Ninguno
   
"""
"""
   \section intro Ejemplo de uso
   En el ejemplo se muestra como utilizar esta libreria
   \verbinclude ejemplo_gamepadv2
"""
class gamepad:
	def __init__(self):
		self.boton=None
		self.direccion={0:None,1:None}
		self.hombre_muerto=None

	def iniciar(self):
		#Aria.init() #No es necesario para funcionar
		gamepad=ArJoyHandler()
		gamepad.init() #Inicializa el gamepad
		gamepad.setSpeeds(100, 700) # revisar que significa en el API
		print gamepad.getNumButtons(), "Numero de botones de la palanca"
		print gamepad.getNumAxes(), "Numero de ejes en la palanca"
		if gamepad.haveJoystick()==False:
			print "No esta conectada la palanca"
			exit(2)#Error tipo 2 se desconecto la palanca
		return gamepad

	def palanca(self,gamepad):
			#Estados de botones
			botones={1:gamepad.getButton(1),
				2:gamepad.getButton(2),
				3:gamepad.getButton(3),
				4:gamepad.getButton(4),
				5:gamepad.getButton(5),
				6:gamepad.getButton(6),
				7:gamepad.getButton(7),
				8:gamepad.getButton(8)}
			#Boton para hombre_muerto
			datos={"b1":1,"b2":2,"b3":3,"b4":4,"l1":5,"r1":6,"l2":7,"r2":8}
			if self.hombre_muerto!=None:
				hombre_muerto=gamepad.getButton(datos[self.hombre_muerto])
				botones[datos[self.hombre_muerto]]='muerto'
			else:
				hombre_muerto=gamepad.getButton(1)
				botones[1]='muerto'
			#
			self.botones=botones # puede utilizarce para remplazar todo el calcula de mas abajo y acondicionar el boton hombre_muerto
			#
			c1=botones[1]
			c2=botones[2]
			c3=botones[3]
			c4=botones[4]
			l1=botones[5]
			r1=botones[6]
			l2=botones[7]
			r2=botones[8]
			eje1=gamepad.getAxis(1) #der-izq 1/-1
			eje2=gamepad.getAxis(2) #Arriba-abajo 1/-1
			#
			if gamepad.haveJoystick()==False:
				exit(2) #Error tipo 2 se desconecto la palanca
			
			if (gamepad.haveJoystick()==True & hombre_muerto==True):
				if eje2!=0:
					if eje2==1:
						self.direccion[0]='ar'
					else:
						self.direccion[0]='ab'
				else:
					self.direccion[0]=None
				if eje1!=0:
					if eje1==1:
						self.direccion[1]='de'
					else:
						self.direccion[1]='iz'
				else:
					self.direccion[1]=None
				if c1==True:
					self.boton='b1' #presiono tecla 1
				elif c2==True:
					self.boton='b2' #presiono tecla 2
				elif c3==True:
					self.boton='b3' #presiono tecla 3
				elif c4==True:
					self.boton='b4' #presiono tecla 4
				elif r1==True:
					self.boton='r1' #presiono tecla R1
				elif r2==True:
					self.boton='r2' #presiono tecla R2
				elif l1==True:
					self.boton='l1' #presiono tecla L1
				elif l2==True:
					self.boton='l2' #presiono tecla L2
			else:
				self.boton=None
				self.direccion={0:None,1:None}

if __name__ == '__main__':
	a=gamepad()
	gamepad=a.iniciar()
	a.hombre_muerto="b1" #si no se selecciona se activa el boton 1 como hombre_muerto
	aa=0
	import time
	while aa!='1':
		a.palanca(gamepad)
		print a.direccion, a.boton
		print a.botones
		time.sleep(10)
		#aa=raw_input("ingrese 1 para salir: ")



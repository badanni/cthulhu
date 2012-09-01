#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       cliente_lib.py
#       
#       Copyright 2012 Danny Enrique Vasconez <dannyvasconeze@gmail.com>
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
"""\package cliente_lib
   \brief libreria para realizar el cliente
   \details Se debe especificar cual es el IP del servidor
   \authors    Danny Vasconez
   \authors   Daniel Granda
   \version   0.0.1
   \date      2012
   \pre       Tener funcionando el servidor
   \bug       Nada
   \warning   uso inapropiado puede hacer que la aplicacion falle
   
"""
"""
   \section intro Ejemplo de uso
   En el ejemplo se muestra tres maneras de enviar comandos la general que es requestOnce y las otras que son la misma pero modificada para trabajar con comandos especificos
   \verbinclude ejemplo_cliente
"""

def main():
	
	return 0

def valores(packet):
	"""
	\brief Sirve cuando se manda el comando "test" en el paquete
	\param packet el paquete que recibe el cliente del servidor 
	\return Nada, pero imprime los valores X,Y,Th en el terminal
	"""
	voltaje_vateria=packet.bufToByte2()/10
	myX = packet.bufToByte4()#
	myY = packet.bufToByte4()
	myTh = packet.bufToByte2()
	myVel = packet.bufToByte2()
	myRotVel = packet.bufToByte2()
	myLatVel = packet.bufToByte2()
	myTemperature = packet.bufToByte()
	print "X= "+str(myX)+" y="+str(myY)+" th="+str(myTh)

def envio_ratioDrive(client,TransRatio,RotRatio,LatRatio):
	"""
	\brief Sirve para realizar la teleoperacion, mandando los parametros 
	\param client Se debe trar el objeto cliente a la definicion para poder utilizar el enlace del cliente para enviar el paquete al servidor
	\param TransRatio Velocidad de traslacion
	\param RotRatio Velocidad de rotacion
	\param LatRatio velocidad lateral para el modelo Pioneer P3-DX no se necesario puede ser 0
	\return client
	"""
	myTransRatio=TransRatio
	myRotRatio=RotRatio
	myLatRatio=LatRatio
	packet=ArNetPacket()
	packet.doubleToBuf(myTransRatio)
	packet.doubleToBuf(myRotRatio)
	packet.doubleToBuf(50) # use half of the robot's maximum.
	packet.doubleToBuf(myLatRatio)
	client.requestOnce("ratioDrive", packet)
	return client
  
def uC_comandos_movi(client,comando,parametro):
	"""
	\brief Sirve para mandar ordenes de movimiento directamente al controlador de la plataforma movil 
	\param client Se debe trar el objeto cliente a la definicion para poder utilizar el enlace del cliente para enviar el paquete al servidor
	\param comando es un numero de 1-255 que representa una funcion esta informacion se puede encontrar en el API de ARIA
	\param parametro el parametro de la funcion en caso de no tener se deja el valor en blanco
	\return client
	"""
	mi_comando=comando #comando 8 es MOVE parametro un valor de 5000 a -4999 es en mm, 11 LEV y su parametro es velocidad +o- mm/s
	mi_parametro=parametro #parametro
	packet=ArNetPacket()
	packet.strToBuf(mi_comando+" "+mi_parametro)
	client.requestOnce("MicroControllerMotionCommand", packet) #MicroControllerMotionCommand
	return client
	
def cliente_inicio(ip="localhost"):
	"""
	\brief Sirve para iniciar la conexion con el servidor
	\param ip="localhost" El valor de local host se lo debe cambiar por el IP del servidor
	\return client
	"""
	client = ArClientBase()
	Aria.init()
	
	startTime = ArTime()
	startTime.setToNow()
	if not client.blockingConnect(ip, 7272): #ip y puerto del servidor
		print "Could not connect to server at localhost port 7272, exiting"
		Aria.exit(1);
	print "cliente: Se tardo %ld msec en connectarse\n" % (startTime.mSecSince())
	
	client.runAsync()
	client.addHandler("updateNumbers",valores) #Verifica y agrega a la cabecera de comandos para el servidor
	if client.dataExists("ratioDrive"): #comprobar si existe el comando ratioDrive
		print "ratioDrive si existe"
	else:
		Aria.exit(1);
	#client=envio_ratioDrive(client,TransRatio,RotRatio,LatRatio) #fijar los valores para mover
	#client=uC_comandos_movi(client,comando,parametro) #Lo hace de una manera directa anulando las demas operaciones
	#client.requestOnce("updateNumbers")
	#client.requestOnce("stop") #parada de emergencia
	return client
def cliente_apaga(client):
	"""
	\brief Sirve para realizar la desconexion con el servidor
	\return Nada
	"""
	ArUtil.sleep(1000)
	client.disconnect()
	ArUtil.sleep(50)
	return 0

class cliente_lib:
	"""
	\class cliente_lib.cliente_lib
	\brief No dispone ninguna utilidad.
	\details  Solo se puso para mantener la estructura de python
	"""
	def __init__(self):
		print "Cargo modulo para cliente_lib"
if __name__ == '__main__':
	main()


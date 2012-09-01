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
   \authors   Danny Vasconez
   \authors   Daniel Granda
   \version   0.0.2
   \date      2012
   \pre       Tener funcionando el servidor
   \bug       myTemperature tiene falla por el tipo de dato en formato a python '\x81' toca pasar a '0x81', devuelve_valors fallo cuando no tiene valores
   \warning   uso inapropiado puede hacer que la aplicacion falle
   
"""
"""
   \section intro Ejemplo de uso
   En el ejemplo se muestra tres maneras de enviar comandos la general que es requestOnce y las otras que son la misma pero modificada para trabajar con comandos especificos
   \verbinclude ejemplo_cliente
"""
class cliente_lib:
	"""
	\class cliente_lib.cliente_lib
	\brief es la clase encargada del cliente 
	\details  se lo utiliza de esta manera par poder trabajar con la informacion tanto leyendo las variables o utilizando los comandos
	"""
	def __init__(self):
		"""
		\brief Carga valores a las variables necesarias para funcionar el cliente
		\details  este comando no es necesario utilizarlo es usado al instanciar la clase
		\param self este parametro no es necesario escribir
		"""
		print "Cargo modulo para cliente_lib"
		self.valor_fisico=[]
		self.valor_sonares=[] 
		self.ip="localhost"
		self.x={}
		self.y={}
		self.t={}
		self.acu=0

	def valores(self,packet):
		"""
		\brief Sirve cuando se manda el comando "updateNumbers" en el paquete
		\details  este comando no es necesario utilizarlo es usado solo por el cliente para procesar el paquete
		\param self este parametro no es necesario escribir
		\param packet el paquete que recibe el cliente del servidor, no es necesario escribir 
		\return Nada, pero guarda en self.valores_fisico [voltaje_bateria,myX,myY,myTh,myVel,myRotVel,myLatVel,myTemperature]
		"""
		#devuelve los valores voltaje_bateria,myX,myY,myTh,myVel,myRotVel,myLatVel,myTemperature
		voltaje_bateria=packet.bufToByte2()/10
		myX = packet.bufToByte4()#
		myY = packet.bufToByte4()
		myTh = packet.bufToByte2()
		myVel = packet.bufToByte2()
		myRotVel = packet.bufToByte2()
		myLatVel = packet.bufToByte2()
		myTemperature = packet.bufToByte()
		#print "X= "+str(myX)+" y="+str(myY)+" th="+str(myTh)
		self.valor_fisico=(voltaje_bateria,myX,myY,myTh,myVel,myRotVel,myLatVel,myTemperature)
		self.valor_fisico=(voltaje_bateria,myX,myY,myTh,myVel,myRotVel,myLatVel,0)
		#print valor

	def lista_sonares(self,packet):
		"""
		\brief Sirve para leer el paquete arNetPacket con la lista del sonar
		\details  este comando no es necesario utilizarlo es usado solo por el cliente para procesar el paquete
		\param self este parametro no es necesario escribir
		\param packet este parametro no es necesario escribir
		\return nada
		"""
		c="                                   "
		numSensor=packet.bufToByte2()
		numSensor2=packet.bufToStr(c,15)
		print str(numSensor)+" "+str(c.strip())

	def valores_sonares(self,packet):
		"""
		\brief Sirve para leer el paquete arNetPacket con los valores del sonar
		\details  este comando no es necesario utilizarlo es usado solo por el cliente para procesar el paquete
		\param self este parametro no es necesario escribir
		\param packet este parametro no es necesario escribir
		\return nada
		"""
		try:
			bandera1=0
			cantidad=packet.bufToDouble()
			print int(cantidad)
			for i in range(2*int(cantidad)):
				if bandera1==0:
					self.x.update({'x%d' % (self.acu):int(packet.bufToByte4())})
					bandera1=1
				else:
					self.y.update({'y%d' % (self.acu):int(packet.bufToByte4())})
					bandera1=0
					self.acu=self.acu+1
				if self.acu==20: #500
					self.acu=0
					self.x={}
					self.y={}
		except:
			print "Fallo lectura sensores"
			self.x={'x0':-9999}
			self.y={'y0':-9999}
			pass

	def envio_ratioDrive(self,client,TransRatio,RotRatio,LatRatio):
		"""
		\brief Sirve para realizar la teleoperacion, mandando los parametros
		\param self este parametro no es necesario escribir
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
	  
	def uC_comandos_movi(self,client,comando,parametro):
		"""
		\brief Sirve para mandar ordenes de movimiento directamente al controlador de la plataforma movil
		\param self este parametro no es necesario escribir
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

	def envio_consulta_fisica(self,client,mensaje):
		"""
		\brief Sirve para mandar ordenes al servidor utilizando paquetes ArNetPacket con comandos <b>pose</b> y  <b>updateNumbers</b>
		\param self este parametro no es necesario escribir
		\param client Se debe trar el objeto cliente a la definicion para poder utilizar el enlace del cliente para enviar el paquete al servidor
		\param mensaje puede ser cualquier comando del servidor que no devuelva informacion a exepcion de pose y updatenumbers
		\return client
		"""
		## se puede usar pose y updateNumbers
		client.requestOnce(mensaje)
		return client
		
	def cliente_inicio(self):
		"""
		\brief Sirve para iniciar la conexion con el servidor
		\param self este parametro no es necesario escribir
		\return client
		"""
		client = ArClientBase()
		#Solo funcionar el lectura de datos por TCP
		client.setTcpOnlyFromServer()
		client.setTcpOnlyToServer()
		#
		Aria.init()
		
		startTime = ArTime()
		startTime.setToNow()
		if not client.blockingConnect(self.ip, 7272): #ip y puerto del servidor
			print "Could not connect to server at %s port 7272, exiting" % self.ip
			
			Aria.exit(1);
		print "cliente: Se tardo %ld msec en connectarse\n" % (startTime.mSecSince())
		
		client.runAsync()
		client.addHandler("updateNumbers",self.valores)
		#
		#client.request("updateNumbers",100)
		#
		client.addHandler("getSensorList",self.lista_sonares)
		client.addHandler("pose",self.valores_sonares)
		#
		#client.lock()
		#client.request("pose",100)
		#client.unlock()
		#
		
		if client.dataExists("ratioDrive"): #supuestamente devuelve la info del robot con odometria
			print "ratioDrive si existe"
		else:
			Aria.exit(1);
		#client=envio_ratioDrive(client,TransRatio,RotRatio,LatRatio) #fijar los valores para mover
		#client=uC_comandos_movi(client,comando,parametro) #Lo hace de una manera directa anulando las demas operaciones
		#client.requestOnce("updateNumbers")
		#client.requestOnce("stop") #parada de emergencia
		return client
	def cliente_apaga(self,client):
		"""
		\brief Sirve para realizar la desconexion con el servidor
		\param self este parametro no es necesario escribir
		\param client para poder desconectar el cliente
		"""
		ArUtil.sleep(1000)
		client.disconnect()
		ArUtil.sleep(50)
		return 0
	def devuelve_valorf(self):
		"""
		\brief Devuelve el variable valor_fisico, con usa espera de 100ms
		\param self este parametro no es necesario escribir
		"""
		ArUtil.sleep(100)
		return self.valor_fisico
	def devuelve_valors(self):
		"""
		\brief Devuelve el variable valor_sonares, con usa espera de 100ms
		\param self este parametro no es necesario escribir
		"""
		ArUtil.sleep(100)
		valor=self.valor_sonares
		if valor==[]:
			print valor
			return {'x0':-9999,'x1':-9999},{'y0':-9999,'y1':-9999},{'t0':0,'t1':0} #valores quitar despues
		else:
			try:
				x_br=[]
				y_br=[]
				t_br=[]
				for a in range(int(valor[0])): #el primer valor indica cuantos elementos se tiene de sensores
					#print valor[1][a]
					valor[1][a]=valor[1][a].strip('(')
					valor[1][a]=valor[1][a].strip(')')
					valor[1][a]=valor[1][a].split(",") #comienza a separar por que viene en forma (X:valor,Y:valor,T:valor)
					valor[1][a][0]=valor[1][a][0].strip() #borrar los espacios en blanco de los elementos
					valor[1][a][1]=valor[1][a][1].strip()
					valor[1][a][2]=valor[1][a][2].strip()
					x_br+=[valor[1][a][0].strip("X:")]
					#print x_br
					y_br+=[valor[1][a][1].strip("Y:")]
					t_br+=[valor[1][a][2].strip("T:")]
					
				#print len(x_br)
				for a in range(len(x_br)):
					self.x.update({'x%d' % self.acu:float(x_br[a])}) #Ordena los datos en forma de diccionario, float tiene problemas con 0.000
					self.y.update({'y%d' % self.acu:float(y_br[a])})
					#self.t.update({'t%d' % self.acu:float(t_br[a].strip(")"))})
					self.t.update({'t%d' % self.acu:0})
					#self.acu+=1
					if self.acu==5000:
						#self.acu=0
						pass
				#print self.x
				#print self.y
				#print self.t
				return self.x,self.y,self.t
			except:
				pass


def main():
	"""
	\brief Sirve para realizar pruebas de conexion 
	\details  sin tener que ejecutar la aplicacion completa; de la siguiente forma "python2.5 cliente_lib.py"
	\return 0
	"""
	#prueba de la libreria
	a=cliente_lib()
	a.ip="192.168.0.124" #Si el servidor esta en otra maquina 
	CLIENTE=a.cliente_inicio()
	#TransRatio,RotRatio,LatRatio = [-50,0,0]
	#CLIENTE=a.envio_ratioDrive(CLIENTE,TransRatio,RotRatio,LatRatio) #fijar los valores para mover
	for i in range(500):
		CLIENTE=a.envio_consulta_fisica(CLIENTE,"pose")
		ArUtil.sleep(500)
		print "Longitud X",len(a.x)
		print "Longitud Y",len(a.y)
	print "X:", a.x
	print "Y:", a.y
		
	CLIENTE.requestOnce("pose")
	ArUtil.sleep(100)
	a.cliente_apaga(CLIENTE)
	return 0
if __name__ == '__main__':
	main()


#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       inicio.py
#       
#       Copyright 2012 Danny Enrique Vasconez <badanni@bzkkx>
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

import pygtk
pygtk.require("2.0")
import gtk
#from time import sleep
import os
import sys
from cliente_lib import *
"""\package inicio
   \brief programa que utiliza la libreria cliente_lib
   \details Programa que utiliza el XML de gtk+ y la libreria cliente_lib para comunicarse con el servidor de la plataforma movil utilizando una interfaz grafica
   \authors   Danny Vasconez
   \authors   Daniel Granda
   \version   0.0.1
   \date      2012
   \pre       Tener funcionando el servidor
   \bug       Nada
   \warning   uso inapropiado puede hacer que la aplicacion falle
   
"""
class prueba_adqui(object):
	"""
	\class inicio.prueba_adqui
	\brief es la clase encargada del entorno grafico y enlace con cliente_lib 
	"""
	def __init__(self):
		"""
		\brief para cargar el XML de gtk+ y sus senales
		\param self no se necesita incluirlo al utilizar la funcion ya que se lo pone solo por ser la definicion de una clase
		\return self
		"""
		builder = gtk.Builder() #El archivo de glade debe estar en gtkbuilder
		builder.add_from_file("glade/GUI.glade") #Carga el archivo glade
		builder.connect_signals(self) #Toma todas las senales de glade
		self.about = builder.get_object("about") #Ventana about
		self.teleoper = builder.get_object("adqui_datos") #Ventana principal
		self.texto_datos = builder.get_object("datos") #boton arriba
		self.texto_datos_sonar = builder.get_object("datos_sonar") #boton arriba
		self.boton_foto = builder.get_object("imagen0") #imagen para el dibujo de la plataforma movil
		self.teleoper.show()
		datos_fisicos=(-11.90,500,4000,-34,15,5,3,14)
		mensaje="Voltaje bateria: %d [V] \nX: %d [mm]\nY: %d [mm]\nTh: %d [grad]\nvelocidad: %d [mm/s]\nVelocidad de giro: %d [rad/s]\nVelocidad lateral: %d [mm/s]\ntemp: %d \n " % (datos_fisicos)
		#[voltaje_bateria,myX,myY,myTh,myVel,myRotVel,myLatVel,myTemperature]
		self.texto_datos.set_text(mensaje)
		#Arranca el cliente
		self.a=cliente_lib()
		self.a.ip="192.168.1.102"
		#print self.a.ip
		self.cliente=self.a.cliente_inicio() 
	def on_menuitem_quit_activate(self, widget, data=None):
		"""
		\brief senal de menu "Salir" y cierra la conexion al salir
		\param self no se necesita incluirlo al utilizar la funcion ya que se lo pone solo por ser la definicion de una clase
		\param widget no se necesita incluirlo al utilizar la funcion ya que se lo pone solo por ser la senal de la interfaz
		param data=None este no es necesario incluirlo ya que viene predefinido con valor None
		\return self
		"""
		print self.a.cliente_apaga(self.cliente)
		gtk.main_quit()
	def on_adqui_datos_destroy(self, widget, data=None):
		"""
		\brief cierra la conexion al cerrar la ventana
		\param self no se necesita incluirlo al utilizar la funcion ya que se lo pone solo por ser la definicion de una clase
		\param widget no se necesita incluirlo al utilizar la funcion ya que se lo pone solo por ser la senal de la interfaz
		param data=None este no es necesario incluirlo ya que viene predefinido con valor None
		\return self
		"""
		print self.a.cliente_apaga(self.cliente)
		gtk.main_quit()
	def on_about_response(self, widget, data=None):
		"""
		\brief cierra la ventana about
		\param self no se necesita incluirlo al utilizar la funcion ya que se lo pone solo por ser la definicion de una clase
		\param widget no se necesita incluirlo al utilizar la funcion ya que se lo pone solo por ser la senal de la interfaz
		\param data=None este no es necesario incluirlo ya que viene predefinido con valor None
		\return self
		"""
		self.about.hide()
	def on_menuitem_abuot_activate(self, widget, data=None):
		"""
		\brief senal de menu about
		\param self no se necesita incluirlo al utilizar la funcion ya que se lo pone solo por ser la definicion de una clase
		\param widget no se necesita incluirlo al utilizar la funcion ya que se lo pone solo por ser la senal de la interfaz
		param data=None este no es necesario incluirlo ya que viene predefinido con valor None
		\return self
		"""
		self.about.show() #Muestra la ventana about
	def on_button1_clicked(self, widget, data=None):
		"""
		\brief senal de boton para leer datos de la plataforma movil
		\param self no se necesita incluirlo al utilizar la funcion ya que se lo pone solo por ser la definicion de una clase
		\param widget no se necesita incluirlo al utilizar la funcion ya que se lo pone solo por ser la senal de la interfaz
		param data=None este no es necesario incluirlo ya que viene predefinido con valor None
		\return self
		"""
		self.cliente=self.a.envio_consulta_fisica(self.cliente,"updateNumbers")
		valor=self.a.devuelve_valorf()
		#toca corregir el dato de temp en cliente_lib '\x81' a '0x81'
		mensaje="Voltaje bateria: %d [V] \nX: %d [mm]\nY: %d [mm]\nTh: %d [grad]\nvelocidad: %d [mm/s]\nVelocidad de giro: %d [rad/s]\nVelocidad lateral: %d [mm/s]\ntemp: %d \n" % (valor)
		#[voltaje_bateria,myX,myY,myTh,myVel,myRotVel,myLatVel,myTemperature]
		self.texto_datos.set_text(mensaje)
		self.cliente=self.a.envio_consulta_fisica(self.cliente,"pose")
		#x,y,t=self.a.devuelve_valors()
		x=self.a.x
		y=self.a.y
		mensaje=''
		for a in range(len(x)):
			mensaje+="sonar="+str(a)+" x="+str(x['x%d' % a])+" y="+str(y['y%d' % a])+"\n"
		self.texto_datos_sonar.set_text(mensaje)
	
def main():
	"""
	\brief El encargado al momento de ejcutar la aplicacion de instanciar el objeto prueba_teleoperacion
	"""
	if os.name=="posix": #verifica que sea un entorno Linux
		app = prueba_adqui() #instancia el objeto GUI con las senales enlazadas
		gtk.main() #levanta el motor GTK para poder visualizar

if __name__ == '__main__':
	main()


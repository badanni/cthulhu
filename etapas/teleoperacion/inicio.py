#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       inicio.py
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
import pygtk
pygtk.require("2.0")
import gtk
#from time import sleep
import os
import sys
from cliente_lib import *
"""\package inicio
   \homepage 
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
class prueba_teleoperacion(object):
	"""
	\class inicio.prueba_teleoperacion
	\brief Se lo crea como objeto para poder trabajar con las senales de la interfaz grafica.
	\details  Y para poder cargar los elementos de la interfaz grafica para el caso que se tengan que ocultar o mostrar
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
		self.teleoper = builder.get_object("teleoperacion") #Ventana principal
		self.boton_up = builder.get_object("up") #boton arriba
		self.boton_right = builder.get_object("right") #boton derch
		self.boton_left = builder.get_object("left") #boton izq
		self.boton_down = builder.get_object("down") #boton abajo
		self.boton_stop = builder.get_object("stop") #boton parar
		self.boton_foto = builder.get_object("imagen0") #imagen para el dibujo de la plataforma movil
		self.teleoper.show()
		self.cliente=cliente_inicio("192.168.0.101")

	def on_up_clicked(self, widget, data=None):
		"""
		\brief senal de click en boton arriba
		\param self no se necesita incluirlo al utilizar la funcion ya que se lo pone solo por ser la definicion de una clase
		\param widget no se necesita incluirlo al utilizar la funcion ya que se lo pone solo por ser la senal de la interfaz
		param data=None este no es necesario incluirlo ya que viene predefinido con valor None
		\return self
		"""
		print "Presiono arriba"
		TransRatio,RotRatio,LatRatio = [50,0,0]
		self.cliente=envio_ratioDrive(self.cliente,TransRatio,RotRatio,LatRatio) #fijar los valores para mover

	def on_down_clicked(self, widget, data=None):
		"""
		\brief senal de click en boton abajo
		\param self no se necesita incluirlo al utilizar la funcion ya que se lo pone solo por ser la definicion de una clase
		\param widget no se necesita incluirlo al utilizar la funcion ya que se lo pone solo por ser la senal de la interfaz
		param data=None este no es necesario incluirlo ya que viene predefinido con valor None
		\return self
		"""
		print "Presiono abajo"
		TransRatio,RotRatio,LatRatio = [-50,0,0]
		self.cliente=envio_ratioDrive(self.cliente,TransRatio,RotRatio,LatRatio) #fijar los valores para mover

	def on_stop_clicked(self, widget, data=None):
		"""
		\brief senal de click en boton parado
		\param self no se necesita incluirlo al utilizar la funcion ya que se lo pone solo por ser la definicion de una clase
		\param widget no se necesita incluirlo al utilizar la funcion ya que se lo pone solo por ser la senal de la interfaz
		param data=None este no es necesario incluirlo ya que viene predefinido con valor None
		\return self
		"""
		print "Presiono alto"
		self.cliente.requestOnce("stop") #parada de emergencia

	def on_left_clicked(self, widget, data=None):
		"""
		\brief senal de click en boton izquierda
		\param self no se necesita incluirlo al utilizar la funcion ya que se lo pone solo por ser la definicion de una clase
		\param widget no se necesita incluirlo al utilizar la funcion ya que se lo pone solo por ser la senal de la interfaz
		param data=None este no es necesario incluirlo ya que viene predefinido con valor None
		\return self
		"""
		print "presiono izquierda"
		TransRatio,RotRatio,LatRatio = [0,90,0]
		self.cliente=envio_ratioDrive(self.cliente,TransRatio,RotRatio,LatRatio) #fijar los valores para mover

	def on_right_clicked(self, widget, data=None):
		"""
		\brief senal de click en boton derecha
		\param self no se necesita incluirlo al utilizar la funcion ya que se lo pone solo por ser la definicion de una clase
		\param widget no se necesita incluirlo al utilizar la funcion ya que se lo pone solo por ser la senal de la interfaz
		param data=None este no es necesario incluirlo ya que viene predefinido con valor None
		\return self
		"""
		print "presiono derecha"
		TransRatio,RotRatio,LatRatio = [0,-90,0]
		self.cliente=envio_ratioDrive(self.cliente,TransRatio,RotRatio,LatRatio) #fijar los valores para mover

	def on_menuitem_abuot_activate(self, widget, data=None):
		"""
		\brief senal de menu about
		\param self no se necesita incluirlo al utilizar la funcion ya que se lo pone solo por ser la definicion de una clase
		\param widget no se necesita incluirlo al utilizar la funcion ya que se lo pone solo por ser la senal de la interfaz
		param data=None este no es necesario incluirlo ya que viene predefinido con valor None
		\return self
		"""
		self.about.show() #Muestra la ventana about

	def on_menuitem_quit_activate(self, widget, data=None):
		"""
		\brief senal de menu "Salir" y cierra la conexion al salir
		\param self no se necesita incluirlo al utilizar la funcion ya que se lo pone solo por ser la definicion de una clase
		\param widget no se necesita incluirlo al utilizar la funcion ya que se lo pone solo por ser la senal de la interfaz
		param data=None este no es necesario incluirlo ya que viene predefinido con valor None
		\return self
		"""
		print cliente_apaga(self.cliente)
		gtk.main_quit()

	def on_teleoperacion_destroy(self, widget, data=None):
		"""
		\brief cierra la conexion al cerrar la ventana
		\param self no se necesita incluirlo al utilizar la funcion ya que se lo pone solo por ser la definicion de una clase
		\param widget no se necesita incluirlo al utilizar la funcion ya que se lo pone solo por ser la senal de la interfaz
		param data=None este no es necesario incluirlo ya que viene predefinido con valor None
		\return self
		"""
		print cliente_apaga(self.cliente)
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

	def main():
		
		return 0

if __name__ == '__main__':
	"""
	\brief El encargado al momento de ejcutar la aplicacion de instanciar el objeto prueba_teleoperacion
	"""
	if os.name=="posix": #verifica que sea un entorno Linux
		app = prueba_teleoperacion() #instancia el objeto GUI con las senales enlazadas
		gtk.main() #levanta el motor GTK para poder visualizar


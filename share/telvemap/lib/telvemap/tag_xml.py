#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       tag_xml.py
#       
#       Copyright 2011 Danny E Vasconez <devch401@ymail.com> archivo original de Icarus
#       Copyright 2012 Danny E. Vasconez <dannyvasconeze@gmail.com> modificado para TelVeMap
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
from xml.dom.minidom import parse 
import datetime, time
import os, sys
#shlex y subprocess correr procesos externos a python como cmd

def leer_valor_configuracion(doc,tagname):
		# El comando devuelve el documento y un valor numerico siendo 0 para cuando no pudo cambiar el nombre
		node = doc.getElementsByTagName(tagname)
		a=0
		valores=[]
		try:
			totales=len(node)
			for i in range(totales):
					valores.extend([node[i].childNodes[0].nodeValue]) 
					a=1
		except:
			a=0
		return doc,valores,a

def cambiar_valor_configuracion(doc,tagname,valor):
		# El comando devuelve el documento y un valor numerico siendo 0 para cuando no pudo cambiar el nombre
		node = doc.getElementsByTagName(tagname)
		a=0
		try:
			totales=len(node)
			for i in range(totales):
					node[i].lastChild.nodeValue=valor
					a=1
		except:
			a=0
		return doc,a

def abrir_archivo(archivo):
		new_file_name = archivo
		old_file_name = new_file_name + "b" 
		os.rename(new_file_name, old_file_name) 
		# change text value of element 
		doc = parse(old_file_name) 
		return doc

def cerrar_archivo(doc,archivo):
		xml_file = open(archivo, "w") 
		doc.writexml(xml_file, encoding="utf-8") 
		xml_file.close() 
		return 0


def main():
	
	return 0

if __name__ == '__main__':
	main()


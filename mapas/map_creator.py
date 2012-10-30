#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       map_creator.py
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



def manual(f):
	aux=1
	f.write("2D-Map\n")
	while aux:
		try:
			LineMinPosX=int(raw_input("LineMinPos X:"))
			LineMinPosY=int(raw_input("LineMinPos Y:"))
			LineMinPos="LineMinPos: %d %d\n" % (LineMinPosX,LineMinPosY)
			aux=0
		except:
			aux=1
	f.write(LineMinPos)
	aux=1
	while aux:
		try:
			LineMaxPosX=int(raw_input("LineMaxPos X:"))
			LineMaxPosY=int(raw_input("LineMaxPos Y:"))
			LineMaxPos="LineMaxPos: %d %d\n" % (LineMaxPosX,LineMaxPosY)
			aux=0
		except:
			aux=1
	f.write(LineMaxPos)
	aux=1
	while aux:
		try:
			NumLines=int(raw_input("NumLines:"))
			Numerodelineas="NumLines: %d\n" % NumLines
			aux=0
		except:
			aux=1
	f.write(Numerodelineas)
	aux=1
	while aux:
		try:
			robotX=int(raw_input("Robot X0:"))
			robotY=int(raw_input("Robot Y0:"))
			robotTh=int(raw_input("Robot Th0:"))
			cairn='Cairn: RobotHome %d %d %d "" ICON "Home"\n' % (robotX,robotY,robotTh)
			aux=0
		except:
			aux=1
	f.write(cairn)
	f.write("LINES\n")
	## for para ingresar las coor de las lineas
	a=NumLines
	print "Primera linea"
	while a>0:
			try:
				x0=int(raw_input("Coordenada X0:"))
				y0=int(raw_input("Coordenada Y0:"))
				x1=int(raw_input("Coordenada X1:"))
				y1=int(raw_input("Coordenada Y1:"))
				coor=str(x0)+" "+str(y0)+" "+str(x1)+" "+str(y1)+"\n"
				f.write(coor)
				a=a-1
			except:
				print "Vuelva a ingresar los valores de las coordenadas (solo numeros enteros)"
			if a>0:
				print "Ingrese la siguiente linea\n"
	f.write("DATA\n")
	f.write("\n")
	mensaje_final="Mapa generado!!"
	print "\n"+mensaje_final
	print "="*len(mensaje_final)
	return f

def automatico(f):
	print "Funcion no implementada"
	return f

if __name__ == '__main__':
	print "Todos los valores estan en [mm]"
	archivo=raw_input("Ingrese el nombre del mapa: ")
	archivo+=".map"
	fileHandle=open(archivo,'w')
	opt='x'
	while opt!='s':
		opt=raw_input("Ingrese 'm' para manual, 'a' para leer los datos de un archivo o 's' para salir: ")
		if opt=='m':
			fileHandle=manual(fileHandle)
			fileHandle.close()
			opt='s'
		elif opt=='a':
			fileHandle=automatico(fileHandle)
			fileHandle.close()
			opt='s'
		elif opt=='s':
			fileHandle.close()
		else:
			print "parametro no valido\n"


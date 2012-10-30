#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       map2svg.py
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



def main():
	archivo=raw_input("Ingrese el nombre del mapa: ")
	archivo1=archivo+".map"
	fileHandle=open(archivo1,'r')
	ListLines=fileHandle.readlines()
	fin = ListLines.index('DATA\n')
	inicio = ListLines.index('LINES\n')
	svg=open(archivo+".svg",'w')
	svg.write('<?xml version="1.0"?>\n')
	svg.write('<svg xmlns="http://www.w3.org/2000/svg">\n')
	for a in range(inicio+1,fin):
		valores=ListLines[a].split(" ")
		mensaje="""    <line x1="%d" 
       y1="%d" 
       x2="%d" 
       y2="%d" 
       style="stroke:blue; stroke-width:1" />\n""" % (int(valores[0]),int(valores[1]),int(valores[2]),int(valores[3]))
		svg.write(mensaje)
	svg.write('</svg>\n')
	fileHandle.close()
	svg.close()

if __name__ == '__main__':
	main()

#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       sem título.py
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
import matplotlib.pyplot as plt
from time import sleep

plt.xlabel('Muestras')
plt.ylabel('Velocidad [mm/s]')
for r in range(100):
	fileHandle=open("dato.txt",'r')
	fileList = fileHandle.readlines()
	a=len(fileList)
	x=range(a)
	y=range(a)
	for i in range(a):
		x[i]=i
		y[i]=float(fileList[i])
	fileHandle.close() 
	
	plt.plot(x,y,'b')
	plt.savefig('alldone'+str(r)+".png", dpi=300,format='png')
	sleep(1)
#plt.show()


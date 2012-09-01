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
from multiprocessing import Process, Queue
from time import sleep
import math

from gamepad import gamepad
from FuzzyController import controlador
from cliente_lib import *

def palanca(c,pipe,msg):
		a=c.gamepad_lectura(pipe,msg)
		if a!=0:
			return a #valor de la palanca
		else:
			return 0
def fuzzy_velocidad(setpoint,ip,a,cliente):
	sol=-1
	try:
		cliente=a.envio_consulta_fisica(cliente,"pose")
		#valor_x,valor_y,valor_t=self.a.devuelve_valors()
		valor_x=a.x
		valor_y=a.y
		#print valor_x, valor_y
		#ArUtil.sleep(100)
		cliente=a.envio_consulta_fisica(cliente,"updateNumbers")
		valores_f=a.devuelve_valorf()
		print 1
		mi_x=valores_f[1]
		mi_y=valores_f[2]
		#print mi_x, mi_y
		#mi_th=self.valores_f[3]
		dato=[]
		if (len(valor_x)>0):
			for a in range(len(valor_x)): #SIP en c. 
				#print math.sqrt(pow(valor_x['x%d' % a]-mi_x,2)+pow(valor_y['y%d' % a]-mi_y,2)), "calculo"
				dato.append(math.sqrt(pow(valor_x['x%d' % a]-mi_x,2)+pow(valor_y['y%d' % a]-mi_y,2)))
			valor_distancia=min(dato) #la distancia mas cercana tomada de la plataforma
			sol=controlador(setpoint,valor_distancia) #Controlador difuso
			if sol<0:
				sol=0
	except:
		#print "Fallo inicio"
		sol='e0'
	print sol
	return sol

def robot_ordenes(Palanca,fuzzy_vel,b,cliente):
	aa=b
	a=palanca(Palanca[0],Palanca[1],Palanca[2])
	vel=fuzzy_velocidad(fuzzy_vel[0],fuzzy_vel[1],fuzzy_vel[2],fuzzy_vel[3])
	if a=="ar":
		print "Arriba",vel
		TransRatio,RotRatio,LatRatio = [vel,0,0]
		cliente=aa.envio_ratioDrive(cliente,TransRatio,RotRatio,LatRatio) #fijar los valores para mover
		ArUtil.sleep(100)
	elif a=="iz":
		print "Izquierda",vel
		TransRatio,RotRatio,LatRatio = [0,vel,0]
		cliente=aa.envio_ratioDrive(cliente,TransRatio,RotRatio,LatRatio) #fijar los valores para mover
		ArUtil.sleep(100)
	elif a=="de":
		print "Derecha",vel
		TransRatio,RotRatio,LatRatio = [0,-vel,0]
		cliente=aa.envio_ratioDrive(cliente,TransRatio,RotRatio,LatRatio) #fijar los valores para mover
		ArUtil.sleep(100)
	elif a=="ab":
		print "Abajo",vel
		TransRatio,RotRatio,LatRatio = [-50,0,0]
		cliente=aa.envio_ratioDrive(cliente,TransRatio,RotRatio,LatRatio) #fijar los valores para mover
		ArUtil.sleep(100)
	elif a=="b1":
		print "B1"
	elif a=="b2":
		print "B2"
	elif a=="b3":
		print "B3"
	elif a=="b4":
		print "B4"
	elif a=="l1":
		print "L1"
	elif a=="l2":
		print "L2"
		aa.requestOnce("stop") #parada de emergencia
		ArUtil.sleep(100)
	elif a=="r1":
		print "R1"
	elif a=="r2":
		print "R2"
	else:
		pass
	#sleep(0.2)
	return a

def main(setpoint,ip=None):
    aa=cliente_lib()
    aa.op=12 #Valores de diccionario de sonares
    if ip!=None:
        aa.ip=ip
    cliente=aa.cliente_inicio()
    c=gamepad()
    try:
       pipe,msg=c.gamepad_init()
       
    except:
       exit()
    fuzzy_vel=[setpoint,ip,aa,cliente]
    palanca=(c,pipe,msg)
    bande='ab'
    #p=Process(target=robot_ordenes, args=(palanca,fuzzy_vel,aa,cliente,))
    #p.start()
    
    while bande!='r2':
      try:
        #p.run()
        bande=robot_ordenes(palanca,fuzzy_vel,aa,cliente)
        #print bande
      except:
        #bande='r2'
        print "error"
        pass
      #sleep(0.2)
    #p.terminate()

if __name__ == '__main__':
    setpoint=150
    ip="192.168.1.102"
    main(setpoint,ip)

#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       multiprocesos.py
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

#Siempre los procesos que compartan queue deben pratabar al mismo tiempo si uno se detiene detien al resto por dejar de existir el queue de este
from multiprocessing import Process, Queue
from time import sleep
import math

from gamepad import gamepad
from FuzzyController import controlador
from cliente_lib import *

def palanca(c,pipe,msg,q):
		a=c.gamepad_lectura(pipe,msg)
		q.put(a)

def fuzzy_velocidad(q,setpoint,a,cliente):
		sol=-1
		try:
			cliente=a.envio_consulta_fisica(cliente,"pose")
			#valor_x,valor_y,valor_t=self.a.devuelve_valors()
			#ArUtil.sleep(100)
			valor_x=a.x
			valor_y=a.y
			#print valor_x, valor_y
			cliente=a.envio_consulta_fisica(cliente,"updateNumbers")
			#ArUtil.sleep(100)
			valores_f=a.devuelve_valorf()
			mi_x=valores_f[1]
			mi_y=valores_f[2]
			#print mi_x, mi_y
			#mi_th=self.valores_f[3]
			dato=[]
			if (len(valor_x)>0):
				for a in range(len(valor_x)):
					dato.append(math.sqrt(pow(valor_x['x%d' % a]-mi_x,2)+pow(valor_y['y%d' % a]-mi_y,2)))
				valor_distancia=min(dato) #la distancia mas cercana tomada de la plataforma
				sol=controlador(setpoint,valor_distancia) #Controlador difuso
				if sol<0:
					sol=0
				q.put(sol)
		except:
			#print "Fallo inicio"
			pass

def robot_ordenes(q,q1,b,cliente):
	aa=b
	a=q.get()
	if q1!=0:
		vel=q1.get()
	else:
		vel='a'
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
		print "B1",vel
	elif a=="b2":
		print "B2",vel
	elif a=="b3":
		print "B3",vel
	elif a=="b4":
		print "B4",vel
	elif a=="l1":
		print "L1",vel
	elif a=="l2":
		print "L2",vel
	elif a=="r1":
		print "R1",vel
	elif a=="r2":
		print "R2",vel
	else:
		pass
	#sleep(0.2)
	return a

def mapa():
	pass

def main(setpoint,ip=None):
    aa=cliente_lib()
    if ip!=None:
       aa.ip=ip
    cliente=aa.cliente_inicio()
    c=gamepad()
    try:
       pipe,msg=c.gamepad_init()
    except:
       aa.Cliente_apaga(cliente)
       exit(1)
    q = Queue() #orden de palanca
    q1 =Queue() #velocidad para el robot
    #anadir info para que tenga datos de trabajo al iniciar
    q.put(1)
    q1.put(-1)
    #comienzo de procesos
    p = Process(target=palanca, args=(c,pipe,msg,q,))
    p1 = Process(target=fuzzy_velocidad, args=(q1,setpoint,aa,cliente,))
    p.start()
    p1.start()
    while 1:
        p1.run()
        p.run()
        a=robot_ordenes(q,q1,aa,cliente)
        if a=="r2":
            break
    p1.terminate()
    p.terminate()
    aa.cliente_apaga(cliente)
    #p.join()
    #p1.join()

if __name__ == '__main__':
    main(150,"192.168.1.102")#150,"192.168.1.102"

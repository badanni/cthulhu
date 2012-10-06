#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       renderizado.py
#       
#       Copyright 2012 Danny Enrique Vasconez <dannyvasconeze@gmail.com>
#                      Daniel Engiberto Granda Guitierrez <degranda87@gmail.com>
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
import cv
from opencv import highgui #Import functions from OpenCV
import os
"""\package renderizado
   \brief programa que utiliza la libreria openCV para la generacion del lienzo 
   \details Programa para realizar el mapa con la informacion del sonar y odometria en la plataforma movil.
   \authors   Danny Vasconez
   \authors   Daniel Granda
   \version   0.0.1
   \date      2012
   \pre       Ningun requisito
   \bug       Si la posicion del robot se sale del lienzo proboca un error en la matriz de la imagen.
   \warning   uso inapropiado puede hacer que la aplicacion falle
   
"""
"""
   \section intro Ejemplo de uso
   En el ejemplo se muestra como se debe utilizar este paquete
   \verbinclude rende_uso
"""
class renderizado():
	"""
	\class renderizado.renderizado
	\brief es la clase encargada de la generacion del mapa atravez de comandos.
	"""
	def __init__(self,dimensiones,nombre_archivo,dimensiones_robot):
		"""
		\brief Inicio de variable de uso de la libreria 
		\param self no se necesita incluirlo al utilizar la funcion ya que se lo pone solo por ser la definicion de una clase
		\param dimensiones Es una tupla con las dimensiones de la imagen a generar
		\param nombre_archivo Es un string con el nombre de la imagen a crear como por ejemplo imagen.jpg
		\param dimensiones_robot Las dimensiones en pixeles de la imagen robot
		\return Nada
		"""
		self.nombre_archivo=nombre_archivo
		self.nombre_archivo1=nombre_archivo.replace(".jpg",".acdc")+".jpg"
		self.dimeniones=dimensiones
		self.dimensiones_robot=dimensiones_robot
		self.image=cv.CreateImage(dimensiones,8,3)
		cv.Not(self.image,self.image)
		cv.SaveImage(self.nombre_archivo1,self.image)
	def cargar(self):
		"""
		\brief genera el los lienzos del mapa y del robot  
		\param self no se necesita incluirlo al utilizar la funcion ya que se lo pone solo por ser la definicion de una clase
		\return Nada
		"""
		self.image=cv.LoadImage(self.nombre_archivo1, cv.CV_LOAD_IMAGE_COLOR) #Load the image
		#
		nombre_archivo="robot.jpg"
		home = os.environ['HOME']
		robot_file = home + "/telvemap/"+nombre_archivo
		#
		self.robot=cv.LoadImage(robot_file, cv.CV_LOAD_IMAGE_COLOR) #Load the image
	def anadir_punto(self,punto,color=0,radio=1):
		"""
		\brief crear un punto en el lienzo del mapa
		\param self no se necesita incluirlo al utilizar la funcion ya que se lo pone solo por ser la definicion de una clase
		\param punto la coordenada donde se va a graficar el circulo
		\param color para cambiar el color del circulo, si no se incluye se grafica en negro
		\param radio para definir el radio del circulo, si no se incluye es tomado como 1
		\return Nada
		"""
		#font = cv.InitFont(cv.CV_FONT_HERSHEY_SIMPLEX, 1, 1, 0, 3, 8) #Creates a font
		#x = 30
		#y = 40
		#cv.PutText(self.image,"Hello World!!!", (x,y),font, 255) #Draw the text
		#cv.Line(image,(a*50,60),9(90,90),cv.RGB(17*a, 110-a, 255))
		cv.Circle(self.image,punto,radio,cv.RGB(255*color, 255*color, 255*color),-1) # ultimo parametro para grosor de la linea negativo lleno
		#self.image1=self.image
	def graficar(self,tiempo_ms,imagen=0):
		"""
		\brief Comando solo utilizado para la prueba del paquete para visualizar los lienzos
		\param self no se necesita incluirlo al utilizar la funcion ya que se lo pone solo por ser la definicion de una clase
		\param tiempo_ms tiempo en milisegundos que se va a mostrar la imagen
		\param imagen es el lienzo que va a ser graficado si no se lo incluye es tomado como cero.
		\return Nada
		"""
		if imagen==0:
			cv.ShowImage('Mapa Robot',self.image) #Show the image
			cv.WaitKey(tiempo_ms)
		else:
			cv.ShowImage('Mapa Robot',imagen) #Show the image
			cv.WaitKey(tiempo_ms)
	def crear_imagen(self):
		"""
		\brief Crea la imagen para cargarla en el programa con el lienzo ya finalizado
		\param self no se necesita incluirlo al utilizar la funcion ya que se lo pone solo por ser la definicion de una clase
		\return Nada
		"""
		cv.SaveImage(self.nombre_archivo1, self.image) #Saves the image#
		
	def rotacion_y_posicion_robot(self,robo_x=200,robo_y=100,robo_th=80):
		"""
		\brief graficar el robot en el lienzo de mapa 
		\param self no se necesita incluirlo al utilizar la funcion ya que se lo pone solo por ser la definicion de una clase
		\param robo_x coordenada x de la odometria del robot 
		\param robo_y coordenada y de la odometria del robot 
		\param robo_th Valor Th del robot
		\return Nada
		"""
		image_mapa=cv.LoadImage(self.nombre_archivo1, cv.CV_LOAD_IMAGE_COLOR)
		dimensiones_robot=self.dimensiones_robot
		image1=cv.CreateImage(dimensiones_robot,8,3)
		image_mascara=cv.CreateImage(dimensiones_robot,8,1)
		
		##rotacion
		#Rotar el robot
		src_center=dimensiones_robot[0]/2,dimensiones_robot[1]/2
		rot_mat=cv.CreateMat( 2, 3, cv.CV_32FC1 )
		cv.GetRotationMatrix2D(src_center, robo_th, 1.0,rot_mat);
		cv.WarpAffine(self.robot,image1,rot_mat)
		#crear filtro para negro
		cv.InRangeS(image1,cv.RGB(0,0,0),cv.RGB(14,14,14),image_mascara)
		cv.Not(image_mascara,image_mascara)
		#cv.ReleaseImage(image1)
		
		#reducir y posicion
		cv.SetImageROI(image_mapa,(robo_x,robo_y, dimensiones_robot[0], dimensiones_robot[1]));
		cv.Copy(image1,image_mapa,mask=image_mascara)
		cv.ResetImageROI(image_mapa);
		
		font = cv.InitFont(cv.CV_FONT_HERSHEY_SIMPLEX, 1, 1, 0, 3, 8) #Creates a font
		#x = 30
		#y = 40
		#cv.PutText(image_mapa,"Posicion robot (x= %d,y= %d,th= %d)" % (robo_x,robo_y,robo_th), (x,y),font, 255) #Draw the text
		
		cv.SaveImage(self.nombre_archivo, image_mapa) #Saves the image#
		#self.graficar(2000,image_mapa)
		return image_mapa
		

if __name__ == '__main__':
	a=renderizado((600,400),"imagen.jpg",(13,13))
	a.cargar()
	for aa in range(5):
		a.anadir_punto((5*aa,5*aa),radio=3*aa)
		a.graficar(500)
	a.crear_imagen()
	a.rotacion_y_posicion_robot(200,100,0)
	a.crear_imagen()
	image_mapa=a.rotacion_y_posicion_robot(20,300,-40)
	a.graficar(100,image_mapa)


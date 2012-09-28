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
"""
Serves files out of its current directory.
Doesn't handle POST requests.
"""
import SocketServer
import SimpleHTTPServer
from cliente_lib import *


#Parametros del servidor web
PORT = 8081

def move(a,b):
    """ sample function to be called via a URL"""
    #Inicio de ARIA y conexion con servidor del robot
    aa = cliente_lib()
    aa.ip="192.168.1.100"
    cliente = aa.cliente_inicio()
    
    TransRatio,RotRatio,LatRatio = [50*a,50*b,0]
    cliente=aa.envio_ratioDrive(cliente,TransRatio,RotRatio,LatRatio)
    
    #apaga cliente
    aa.cliente_apaga(cliente)
    
    return 'hi'+str(a)+" "+str(b)
def adelante():
    return 'vamos!!!'
def prueba():
    valor="""hola</br>como estas? esto es una prueba?</br>si valio la conexion
    """
    return valor

class CustomHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):

    def do_GET(self):
        
        #Sample values in self for URL: http://localhost:8080/jsxmlrpc-0.3/
        #self.path  '/jsxmlrpc-0.3/'
        #self.raw_requestline   'GET /jsxmlrpc-0.3/ HTTP/1.1rn'
        #self.client_address    ('127.0.0.1', 3727)
        if self.path=='/atras':
            #This URL will trigger our sample function and send what it returns back to the browser
            self.send_response(200) #200
            self.send_header('Content-type','text/html')
            self.end_headers()
            self.wfile.write(move(-1,0)) #call sample function here
            return
        elif self.path=='/adelante':
            #This URL will trigger our sample function and send what it returns back to the browser
            self.send_response(20)
            self.send_header('Content-type','text/html')
            self.end_headers()
            self.wfile.write(move(1,0)) #call sample function here
            return
        elif self.path=='/derecha':
            #This URL will trigger our sample function and send what it returns back to the browser
            self.send_response(200)
            self.send_header('Content-type','text/html')
            self.end_headers()
            self.wfile.write(move(0,1)) #call sample function here
            return
        elif self.path=='/izquierda':
            #This URL will trigger our sample function and send what it returns back to the browser
            self.send_response(200)
            self.send_header('Content-type','text/html')
            self.end_headers()
            self.wfile.write(move(0,-1)) #call sample function here
            return
        elif self.path=='/prueba':
            #This URL will trigger our sample function and send what it returns back to the browser
            self.send_response(200)
            self.send_header('Content-type','text/html')
            self.end_headers()
            self.wfile.write(prueba()) #call sample function here
            return
        else:
            #serve files, and directory listings by following self.path from
            #current working directory
            SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

Aria.init()

httpd = SocketServer.ThreadingTCPServer(("192.168.1.101", PORT),CustomHandler)

print "serving at port", PORT
httpd.serve_forever()

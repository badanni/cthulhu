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

PORT = 8081

def move():
    """ sample function to be called via a URL"""
    return 'hi'
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
        if self.path=='/move':
            #This URL will trigger our sample function and send what it returns back to the browser
            self.send_response(200)
            self.send_header('Content-type','text/html')
            self.end_headers()
            self.wfile.write(move()) #call sample function here
            return
        elif self.path=='/adelante':
            #This URL will trigger our sample function and send what it returns back to the browser
            self.send_response(200)
            self.send_header('Content-type','text/html')
            self.end_headers()
            self.wfile.write(adelante()) #call sample function here
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
    def do_POST(self):
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        self.wfile.write(adelante()) #call sample function here
        return

httpd = SocketServer.ThreadingTCPServer(("", PORT),CustomHandler)

print "serving at port", PORT
httpd.serve_forever()

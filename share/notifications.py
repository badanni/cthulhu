#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       untitled.py
#       
#       Copyright 2012 Danny E Vasconez <badanni@badanni-Inspiron-N5110>
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
#!/usr/bin/env python
try:
    import gtk, pygtk, os, os.path, pynotify
    pygtk.require('2.0')
except:
    print "Error: need python-notify, python-gtk2 and gtk"

def mensaje(a):
    #n = pynotify.Notification("Moo title", "test")
    home = os.environ['HOME']
    dst = os.path.join(home+"/telvemap/", "icon.png")
    n = pynotify.Notification("Moo title", "test "+str(a), "file:///"+dst)#"file:///home/badanni/icon.png")
    n.set_urgency(pynotify.URGENCY_CRITICAL)
    n.set_timeout(100) # en milisegundos
    #n.set_category("device")

    if not n.show():
        print "Failed to send notification"
        sys.exit(1)

if __name__ == '__main__':
    if not pynotify.init("Timekpr notification"):
        sys.exit(1)
    for a in range(10):
      mensaje(a)


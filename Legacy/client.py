# -*- coding: utf-8 -*-
"""
Created on Sat Aug 24 12:47:32 2019

@author: zfern
"""

#!/usr/bin/env python

import socket


TCP_IP = "104.155.186.224" 
TCP_PORT = 5005
BUFFER_SIZE = 1024
MESSAGE = "Hello, World!".encode()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
s.send(MESSAGE)
data = s.recv(BUFFER_SIZE)
s.close()

print ("received data:", data)

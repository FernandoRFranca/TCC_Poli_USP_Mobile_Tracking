# -*- coding: utf-8 -*-
"""
Created on Sat Aug 24 12:06:39 2019

@author: zfern
"""

#Programa que escreve dados fake em txt.

k = 0

with open("teste.txt",'w') as file:
    while (k<=10):
        if (k==0):
            file.write("Primary Key\n")
            k = k + 1
        else:
            file.write(str(k)+"\n")
            k = k + 1
file.close()


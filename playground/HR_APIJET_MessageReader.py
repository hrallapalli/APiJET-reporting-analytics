# -*- coding: utf-8 -*-
"""
Created on Fri Apr  2 13:44:56 2021

@author: Hari.rallapalli
"""
import xml.etree.ElementTree as ET
import re


filename = r'C:\Users\Hari.rallapalli\Desktop\APIJET\TAPEngine_MessagingLog_L_APIJET02_asteroid_20210303_165510.xml'


with open(filename,'r', encoding='utf-8') as myFile:
    myFile=myFile.read()
    if "#" in myFile:
        myFile = re.sub(r'<#.+?#>', '', myFile)
    myFile = myFile + '</TapMessagingLog>'
 
root = ET.fromstring(myFile)

children = root.getchildren()

for child in children:
    ET.dump(child)
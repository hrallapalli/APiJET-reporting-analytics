#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 23 17:15:43 2021

@author: vinh.bui
"""

import pandas as pd

#Input and output file name


input_file  = "TAPEngine_MessagingLog_L_APIJET02_asteroid_20210402_022848.xml"
output_file = "FDX_1276_JFK_MEM_ROUTE_DATA"


file = open(input_file,'r')

content = file.readlines()

route_data = []

for lines in content: 
    if 'ROUTE_DATA' in lines: 
        route_data.append(lines)


df = pd.DataFrame(route_data, columns = ['Route Data'])
df = df["Route Data"].str.split(">", n = 1000, expand = True)


column_count = len(df.columns)
b = ['Column_'+str(i) for i in range(0, column_count)]
df.columns = b

#df = df.drop(columns = ['Column_0','Column_1','Column_2','Column_3','Column_4'])

df.drop(df.iloc[:, 0:10], inplace = True, axis = 1)

df = df.transpose()

column_num = len(df.columns)
c = ['Column_'+str(i) for i in range(0, column_num)]
df.columns = c

df = df[df["Column_0"].str.contains("ALTERNATE")==False]

df = df.transpose()
df = df.drop_duplicates()

df.to_excel(output_file + ".xlsx", index = False)









        


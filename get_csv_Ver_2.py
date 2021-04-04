#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  1 11:36:56 2021

@author: vinh.bui
"""

import os 

import shutil

#Directory to where all your output folders that data_translator.exe creates 

source_dir = r"C:\Users\vinh.bui\Desktop\All_Flight_Test\Finished_runs"

#Directory to where you want all your CSV files to go 

target_dir = r"C:\Users\vinh.bui\Desktop\All_Flight_Test\Benefit_CSV"

#You can create any variable and assign the ending of the CSV file that you want to extract
#after you have that ending created, create a new "try" function inside the "for" loop
#like code below to get the CSV files that will help you with your analysis 


aop_traj = 'AopOwnshipTrajectoryDataRecord.csv'

aop_state = 'AopOwnshipStateDataRecord.csv'

aop_route = 'AopRouteDataRecord.csv'

tap_refresh = 'TapAdvisoryRefreshDataRecord.csv'

tap_traj =  'TapAdvisoryTrajectoryDataRecord.csv'

tap_route = 'TapRouteDataRecord.csv'

for root, dirs, files in os.walk((os.path.normpath(source_dir)), topdown = False):
    try:
        for file in files: 
            if file.endswith(aop_traj):
                print("Found them")
                source_folder = os.path.join(root, file)
                shutil.copy2(source_folder, target_dir)
                
    except Exception as e: 
        print(e) 
        
    try:
        for file in files: 
            if file.endswith(aop_state):
                print("Found them")
                source_folder = os.path.join(root, file)
                shutil.copy2(source_folder, target_dir)
                
    except Exception as e: 
        print(e) 
        
    try:
        for file in files: 
            if file.endswith(aop_route):
                print("Found them")
                source_folder = os.path.join(root, file)
                shutil.copy2(source_folder, target_dir)
            
    except Exception as e: 
        print(e) 
     
                
    try:
        for file in files: 
            if file.endswith(tap_refresh):
                print("Found them")
                source_folder = os.path.join(root, file)
                shutil.copy2(source_folder, target_dir)
                
    except Exception as e: 
        print(e) 
        
    try:
        for file in files: 
            if file.endswith(tap_route):
                print("Found them")
                source_folder = os.path.join(root, file)
                shutil.copy2(source_folder, target_dir)
            
    except Exception as e: 
        print(e) 
                  
    try:
        for file in files: 
            if file.endswith(tap_traj):
                print("Found them")
                source_folder = os.path.join(root, file)
                shutil.copy2(source_folder, target_dir)
                
    except Exception as e: 
        print(e)                
                    
                    
                    



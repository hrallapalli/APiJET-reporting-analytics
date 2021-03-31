 # -*- coding: utf-8 -*-

import os

import HR_APIJET_AopRouteDataRecord_Parser as rp
import HR_APIJET_AopOwnshipStateDataRecord_Parser as sp
import HR_APIJET_AopTrajectoryDataRecord_Parser as tp
import HR_APIJET_RouteToTrajectoryAlignment as r2ta
import HR_APIJET_Aligned_TrajToState_Deviation as t2sd


rootdir = r'C:\Users\Hari.rallapalli\Desktop\APIJET\loopingtest'

for flight_folder in os.listdir(rootdir):
    print(('Current flight:', flight_folder))
    out_dir_path = os.path.join(rootdir,flight_folder,'analysis')
    
    if not os.path.exists(out_dir_path):
        os.makedirs(out_dir_path)
        print('analysis output path created')
    else:
        print('analysis output path already exists')
    
    try:
        pathToRoute = os.path.join(rootdir,flight_folder,'AopRouteDataRecord.csv')
        pathToTraj  = os.path.join(rootdir,flight_folder,'AopOwnshipTrajectoryDataRecord.csv')
        pathToState = os.path.join(rootdir,flight_folder,'AopOwnshipStateDataRecord.csv')
    except:
        print('Incorrect formatting of input .csv filenames or unsuitable root directory')
    
    r2ta.AlignedTraj(pathToRoute, pathToTraj, out_dir_path)
    
    pathToAlignedTraj = os.path.join(out_dir_path,'ROUTEALIGNED_AopOwnshipTrajectoryDataRecord.csv')
    t2sd.RouteToStateDeviations(pathToState, pathToAlignedTraj,out_dir_path)
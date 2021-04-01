 # -*- coding: utf-8 -*-

import os
import shutil
# import subprocess
# import rpy2.robjects as robjects

import HR_APIJET_RouteToTrajectoryAlignment as r2ta
import HR_APIJET_Aligned_TrajToState_Deviation as t2sd

rootdir = r'C:\Users\Hari.rallapalli\Desktop\APIJET\loopingtest'
rscriptdir = r'C:\Users\Hari.rallapalli\Desktop\APIJET\APIJET_flight_deviations_analysis.Rmd'
rknitdir = r'C:\Users\Hari.rallapalli\Desktop\APIJET\knit_analysis.R'

for flight_folder in os.listdir(rootdir):
    print(('Current flight:', flight_folder))
    out_dir_path = os.path.join(rootdir,flight_folder,'analysis')
    
    if not os.path.exists(out_dir_path):
        os.makedirs(out_dir_path)
        print('analysis output path created')
    else:
        print('analysis output path already exists')
    
    try:
        pathToRoute = os.path.join(rootdir,flight_folder,(flight_folder,'_AopRouteDataRecord.csv'))
        pathToTraj  = os.path.join(rootdir,flight_folder,(flight_folder,'_AopOwnshipTrajectoryDataRecord.csv'))
        pathToState = os.path.join(rootdir,flight_folder,(flight_folder,'_AopOwnshipStateDataRecord.csv'))
    except:
        print('Incorrect formatting of input .csv filenames or unsuitable root directory')
    
    r2ta.AlignedTraj(pathToRoute, pathToTraj, out_dir_path)
    
    pathToAlignedTraj = os.path.join(out_dir_path,'ROUTEALIGNED_AopOwnshipTrajectoryDataRecord.csv')
    t2sd.RouteToStateDeviations(pathToState, pathToAlignedTraj,out_dir_path)
    
    shutil.copy(rscriptdir, out_dir_path)
    shutil.copy(rknitdir, out_dir_path)
    
    # os.chdir(out_dir_path)
    # robjects.r.source("knit_analysis.R")

    # subprocess.call([r'C:\Users\Hari.rallapalli\Anaconda3\envs\rstudio\lib\R\bin\Rscript', '--vanilla','knit_analysis.R'], shell=True)
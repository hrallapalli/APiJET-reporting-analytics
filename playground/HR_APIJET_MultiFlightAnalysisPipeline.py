 # -*- coding: utf-8 -*-

import os
import shutil
import subprocess
import datetime as dt
# import rpy2.robjects as robjects

import HR_APIJET_RouteToTrajectoryAlignment as r2ta
import HR_APIJET_Aligned_TrajToState_Deviation as t2sd
import HR_APIJET_DistanceAligned_FuelAndTime_Deviations as FaT
import HR_APIJET_TapAdvisoryParser as TAP

# rootdir = r'C:\Users\Hari.rallapalli\Desktop\APIJET\loopingtest'
# rootdir = r'\\ijet-file-01.us.ijetonboard.com\Engineering\FedEx Trial DAT\Finished_run_20210315'

rootdir = r'C:\Users\Hari.rallapalli\OneDrive - APiJET\Desktop\APIJET\20210423_test'
rscriptdir = r'C:\Users\Hari.rallapalli\OneDrive - APiJET\Desktop\APIJET\APIJET_flight_deviations_analysis.Rmd'
rknitdir = r'C:\Users\Hari.rallapalli\OneDrive - APiJET\Desktop\APIJET\knit_analysis.R'

dt = dt.datetime.now()
ts = str(round(dt.timestamp()*1000))

for flight_folder in os.listdir(rootdir):
    if flight_folder.startswith('.'):
        continue
    elif flight_folder == 'Temp':
        continue
    elif flight_folder.endswith('.xlsx'):
        continue
    
    print(('Current flight:', flight_folder))
    out_dir_path = os.path.join(rootdir,flight_folder,'analysis_' + ts)
    
    if not os.path.exists(out_dir_path):
        os.makedirs(out_dir_path)
        print('analysis output path created')
    else:
        shutil.rmtree(out_dir_path)
        os.makedirs(out_dir_path)
        print('analysis output path already exists! Overwriting!')
    
    try:
        pathToRoute = os.path.join(rootdir,flight_folder,(flight_folder + '_AopRouteDataRecord.csv'))
        pathToTraj  = os.path.join(rootdir,flight_folder,(flight_folder +'_AopOwnshipTrajectoryDataRecord.csv'))
        pathToState = os.path.join(rootdir,flight_folder,(flight_folder +'_AopOwnshipStateDataRecord.csv'))
        pathToAdvisory = os.path.join(rootdir,flight_folder,(flight_folder +'_TapAdvisoryRefreshDataRecord.csv'))
    except:
        print('Incorrect formatting of input .csv filenames or unsuitable root directory')
    
    r2ta.AlignedTraj(pathToRoute, pathToTraj, out_dir_path)
    
    pathToAlignedTraj = os.path.join(out_dir_path,'ROUTEALIGNED_AopOwnshipTrajectoryDataRecord.csv')
    t2sd.RouteToStateDeviations(pathToState, pathToAlignedTraj,out_dir_path)
    
    FaT.FuelAndTimeDeviations(pathToState, pathToAlignedTraj,out_dir_path)
    TAP.TapAdvisoryParser(pathToAdvisory,out_dir_path)
    
    shutil.copy(rscriptdir, out_dir_path)
    shutil.copy(rknitdir, out_dir_path)
    
    # os.chdir(out_dir_path)
    # robjects.r.source("knit_analysis.R")

    # subprocess.call([r'C:\Users\Hari.rallapalli\Anaconda3\envs\rstudio\lib\R\bin\Rscript', '--vanilla','knit_analysis.R'], shell=True)
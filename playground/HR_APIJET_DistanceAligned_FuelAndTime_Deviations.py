# -*- coding: utf-8 -*-
"""
@author: Hari.rallapalli
"""
from shapely.geometry import Point, MultiPoint
from shapely.ops import nearest_points
import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
import HR_APIJET_AopOwnshipStateDataRecord_Parser as sp


def FuelAndTimeDeviations(pathToStateFile, pathToAlignedTraj,outputPath):

    State_df = sp.StateParser(pathToStateFile)
    Traj_df = pd.read_csv(pathToAlignedTraj)

    waypoints = []
    pred_weight = []
    pred_time = []
    
    for n in range(len(Traj_df)):
        waypoints.append((Point(Traj_df.Longitude[n], Traj_df.Latitude[n])))
        pred_weight.append(Traj_df.Weight[n])
        pred_time.append(Traj_df.Timestamp[n])
        
    
    statepoints = []
    for n in range(len(State_df)):
       statepoints.append(Point(State_df.LongitudePresent[n], State_df.LatitudePresent[n]))
        
    State_df['StatePoints'] = statepoints
    state_multipoints = MultiPoint(statepoints)

    nearest_state = []
    state_weight = []
    state_time = []
    
    for n,traj_point in enumerate(waypoints):
        
        nearest_geoms = nearest_points(traj_point, state_multipoints)
        
        nearest_state.append(nearest_geoms[1])
        
        try:
            filtered_State_df = State_df.loc[State_df['StatePoints'] == nearest_geoms[1]]
            state_weight.append(filtered_State_df['AircraftWeight'].iloc[0])
            state_time.append(filtered_State_df['Timestamp'].iloc[0])
        except:
            print("you've got some serious problems... there is more than one closest point somehow. How did you fuck this up?")

    

    devi_weight = np.subtract(state_weight,pred_weight)
    devi_time = np.subtract(state_time,pred_time)
    
    
    
    xs = [point.x for point in waypoints]
    ys = [point.y for point in waypoints]
    plt.figure()
    plt.title('Time Deviation (seconds)')
    plt.set_cmap('RdYlGn_r')
    plt.scatter(xs,ys,c=devi_time, label = "time savings")
    plt.colorbar()
    plt.savefig(os.path.join(outputPath,'Time_Deviation.png'), transparent = True, dpi = 300)
    
    plt.figure()
    plt.title('Weight Deviation (pounds)')
    plt.set_cmap('RdYlGn')
    plt.scatter(xs,ys,c=devi_weight, label = "fuel savings")
    plt.colorbar()
    plt.savefig(os.path.join(outputPath,'Fuel_Deviation.png'), transparent = True, dpi = 300)
    
    FuelAndTimeDeviations_frame = pd.DataFrame()
    
    FuelAndTimeDeviations_frame["pred_points"] = waypoints
    FuelAndTimeDeviations_frame["pred_weight"] = pred_weight
    FuelAndTimeDeviations_frame["pred_time"] = pred_time
    FuelAndTimeDeviations_frame["nearest_state"] = nearest_state
    FuelAndTimeDeviations_frame["state_weight"] = state_weight
    FuelAndTimeDeviations_frame["state_time"] = state_time
    FuelAndTimeDeviations_frame["devi_weight"] = devi_weight
    FuelAndTimeDeviations_frame["devi_time"] = devi_time
    
    
    FuelAndTimeDeviations_frame.to_csv(os.path.join(outputPath,'DEVIATIONS_FuelAndTime.csv'))
    
    return FuelAndTimeDeviations_frame

if __name__ == '__main__':
    df = FuelAndTimeDeviations(r'C:\Users\Hari.rallapalli\OneDrive - APiJET\Desktop\APIJET\20210423_test\Flight_Run_0\Flight_Run_0_AopOwnshipStateDataRecord.csv',r'C:\Users\Hari.rallapalli\OneDrive - APiJET\Desktop\APIJET\20210423_test\Flight_Run_0\analysis_1619201197326\ROUTEALIGNED_AopOwnshipTrajectoryDataRecord.csv',r'C:\Users\Hari.rallapalli\OneDrive - APiJET\Desktop\APIJET\20210423_test\Flight_Run_0\analysis_1619201197326')

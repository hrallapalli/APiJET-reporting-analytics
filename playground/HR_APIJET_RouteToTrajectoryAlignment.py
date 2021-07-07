# -*- coding: utf-8 -*-
"""
Created on Thu Mar  4 00:19:43 2021

@author: Hari Rallapalli
"""
import pandas as pd
import os

import HR_APIJET_AopRouteDataRecord_Parser as rp
import HR_APIJET_AopTrajectoryDataRecord_Parser as tp

def AlignedTraj(pathToRoute, pathToTraj, outputPath):
        
    def TakeClosestGreater(number, collection):
        closest_greater_value = collection[collection > number].min()  
        return closest_greater_value
    
    def TrajectoryLifetime(timepoints, lasttime):
        diff_list = []
        for x, y in zip(timepoints[0::], timepoints[1::]):
            diff_list.append(y-x)
            
        for n,x in enumerate(diff_list):
            if x == 0:
                try:
                    diff_list[n]=diff_list[n+1]
                except:
                    continue
        diff_list.append(lasttime-timepoints[-1])
        return diff_list
    
    # Route_df = pd.read_csv(pathToRoute)
    # Traj_df = tp.TrajParser(pathToTraj)
    
    # Route_WallTime_Check = []
    
    # Traj_First_WallTime = Traj_df["WallTime"].iloc[0]
    # Traj_Closest_ID = []
    # Traj_Closest_WallTime = []
    
    # #########
    # # Filtering Route data printed before first Trajectory update (by SimTime) 
    # #########
    
    # Route_First_Traj_ind = Route_df["Wall_Time"] > Traj_First_WallTime
    # Route_df = Route_df[Route_First_Traj_ind]
    
    # #########
    # # End of filtering
    # #########
    
    # stitch_Traj_df = pd.DataFrame(columns = Traj_df.columns)
    
    # for n in range(len(Route_df)):
        
    #     try:
    #         Start_Walltime = Route_df["Wall_Time"].iloc[n]
    #         Finish_Walltime = Route_df["Wall_Time"].iloc[n]
    #     except:
    #         Start_Walltime = Route_df["Wall_Time"].iloc[n]
    #         Finish_Walltime = 2147483647 # This is the max 32-bit number. Will need to update when 64-bit timestamps are implemented.
        
    #     closest_WallTime = TakeClosestGreater(Start_Walltime, Traj_df["WallTime"])
    #     filtered_Traj_df = Traj_df[Traj_df["WallTime"] == closest_WallTime]
            
    #     tmp_Traj_df = filtered_Traj_df[(filtered_Traj_df['Timestamp'] >= closest_WallTime) & (filtered_Traj_df['Timestamp'] <= Finish_Walltime)]
    #     stitch_Traj_df = pd.concat([stitch_Traj_df,tmp_Traj_df]).drop_duplicates().reset_index(drop=True)
        
        
    Route_df = rp.RouteParser(pathToRoute)
    Traj_df = tp.TrajParser(pathToTraj)
    
    Route_SimTime_Check = []
    
    Traj_First_Simtime = Traj_df["SimTime"].iloc[0]
    Traj_Closest_ID = []
    Traj_Closest_SimTime = []
    
    
    #########
    # Filtering Route data printed before first Trajectory update (by SimTime) 
    #########
    
    Route_First_Traj_ind = Route_df["SimTime"] > Traj_First_Simtime
    Route_df = Route_df[Route_First_Traj_ind]
    
    if len(Route_df) == 0:
        return
    
    #########
    # End of filtering
    #########
    
    for (n,FlightPlan) in enumerate(Route_df["APIJET_FLIGHTPLAN_WAYPOINT_IDENTIFIER"].unique()):
        is_FlightPlan = Route_df["APIJET_FLIGHTPLAN_WAYPOINT_IDENTIFIER"]==FlightPlan
        
        Route_df_FlightPlan = Route_df[is_FlightPlan]
        
        Route_SimTime_Check.append(Route_df_FlightPlan["SimTime"].iloc[0])
        try:
            Traj_Closest_SimTime.append(TakeClosestGreater(Route_SimTime_Check[n],Traj_df["SimTime"]))
            Traj_Closest = Traj_df[Traj_df["SimTime"]==Traj_Closest_SimTime[n]]
            Traj_Closest_ID.append(Traj_Closest["TrajId"].iloc[0])
        except:
            Traj_Closest_SimTime = Traj_Closest_SimTime[:-1]
            print('Route change occurs after Trajectory stops printing!')
            continue
    
    Traj_Last_SimTime = Traj_df["SimTime"].iloc[-1]
    Traj_Difflist = TrajectoryLifetime(Traj_Closest_SimTime,Traj_Last_SimTime)
    
    Traj_Furthest_SimTime = [Traj_Closest_SimTime[i]+Traj_Difflist[i] for i in range(len(Traj_Closest_SimTime))]
    
    stitch_Traj_df = pd.DataFrame(columns = Traj_df.columns)
    
    for n,time in enumerate(Traj_Closest_SimTime):
        isTrajId = Traj_df["TrajId"]==Traj_Closest_ID[n]
        filtered_Traj_df = Traj_df[isTrajId]
        
        tmp_Traj_df= filtered_Traj_df[(filtered_Traj_df['Timestamp'] >= Traj_Closest_SimTime[n]) & (filtered_Traj_df['Timestamp'] <= Traj_Furthest_SimTime[n])]
        stitch_Traj_df = pd.concat([stitch_Traj_df,tmp_Traj_df]).drop_duplicates().reset_index(drop=True)
    
    stitch_Traj_df.to_csv(os.path.join(outputPath,'ROUTEALIGNED_AopOwnshipTrajectoryDataRecord.csv'))
    
    return stitch_Traj_df

if __name__ == '__main__':
    AlignedTraj_df = AlignedTraj(r'C:\Users\Hari.rallapalli\Desktop\APIJET\test_flight_JFK-MEM\flightplan_changes.csv',r'C:\Users\Hari.rallapalli\Desktop\APIJET\test_flight_JFK-MEM\MEM_JFK_1431_7AprAopOwnshipTrajectoryDataRecord.csv',r'C:\Users\Hari.rallapalli\Desktop\APIJET\test_flight_JFK-MEM\analysis')

# -*- coding: utf-8 -*-
"""
Created on Thu Mar  4 00:19:43 2021

@author: Hari Rallapalli
"""
import pandas as pd

import HR_APIJET_AopRouteDataRecord_Parser as rp
import HR_APIJET_AopTrajectoryDataRecord_Parser as tp

def AlignedTraj():
        
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
    
    
    Route_df = rp.RouteParser()
    Traj_df = tp.TrajParser()
    
    Route_SimTime_Check = []
    
    Traj_First_Simtime = Traj_df["SimTime"].iloc[0]
    Traj_Closest_ID = []
    Traj_Closest_SimTime = []
    
    
    #########
    # Filtering Route data printed before first Trajectory update (by SimTime) 
    #########
    
    Route_First_Traj_ind = Route_df["SimTime"] > Traj_First_Simtime
    Route_df = Route_df = Route_df[Route_First_Traj_ind]
    
    #########
    # End of filtering
    #########
    
    for (n,FlightPlan) in enumerate(Route_df["APIJET_FLIGHTPLAN_WAYPOINT_IDENTIFIER"].unique()):
        is_FlightPlan = Route_df["APIJET_FLIGHTPLAN_WAYPOINT_IDENTIFIER"]==FlightPlan
        
        Route_df_FlightPlan = Route_df[is_FlightPlan]
        
        Route_SimTime_Check.append(Route_df_FlightPlan["SimTime"].iloc[0])
        
        Traj_Closest_SimTime.append(TakeClosestGreater(Route_SimTime_Check[n],Traj_df["SimTime"]))
        Traj_Closest = Traj_df[Traj_df["SimTime"]==Traj_Closest_SimTime[n]]
        Traj_Closest_ID.append(Traj_Closest["TrajId"].iloc[0])
    
    Traj_Last_SimTime = Traj_df["SimTime"].iloc[-1]
    Traj_Difflist = TrajectoryLifetime(Traj_Closest_SimTime,Traj_Last_SimTime)
    
    Traj_Furthest_SimTime = [Traj_Closest_SimTime[i]+Traj_Difflist[i] for i in range(len(Traj_Closest_SimTime))]
    
    stitch_Traj_df = pd.DataFrame(columns = Traj_df.columns)
    
    for n,time in enumerate(Traj_Closest_SimTime):
        isTrajId = Traj_df["TrajId"]==Traj_Closest_ID[n]
        filtered_Traj_df = Traj_df[isTrajId]
        
        tmp_Traj_df= filtered_Traj_df[(filtered_Traj_df['Timestamp'] >= Traj_Closest_SimTime[n]) & (filtered_Traj_df['Timestamp'] <= Traj_Furthest_SimTime[n])]
        stitch_Traj_df = pd.concat([stitch_Traj_df,tmp_Traj_df]).drop_duplicates().reset_index(drop=True)
    
    stitch_Traj_df.to_csv(r'ROUTEALIGNED_AopOwnshipTrajectoryDataRecord.csv')
    
    return stitch_Traj_df

if __name__ == '__main__':
    AlignedTraj_df = AlignedTraj()

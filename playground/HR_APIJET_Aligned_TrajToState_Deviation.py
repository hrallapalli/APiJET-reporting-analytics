# -*- coding: utf-8 -*-
"""
@author: Hari.rallapalli
"""
from shapely.geometry import Point, Polygon, LineString
import pandas as pd
import os

import HR_APIJET_AopOwnshipStateDataRecord_Parser as sp
import HR_APIJET_RouteToTrajectoryAlignment as tp

def RouteToStateDeviations(pathToStateFile, pathToAlignedTraj,outputPath):

    State_df = sp.StateParser(pathToStateFile)
    # Traj_df = tp.AlignedTraj(pathToRouteFile,pathToAlignedTraj,outputPath)
    Traj_df = pd.read_csv(pathToAlignedTraj)
    
    
    waypoints = []
    altitudes = []
    for n in range(len(Traj_df)):
        waypoints.append((Point(Traj_df.Longitude[n], Traj_df.Latitude[n])))
        altitudes.append(Point(0,Traj_df.Altitude[n]))
        
    optimal_trajectory = LineString(waypoints)
    optimal_altitudes = LineString(altitudes)
    
    ac_positions = []
    ac_altitudes = []
    latlong_distances = []
    altitude_distances = []
    
    for n in range(len(State_df)):
        ac_positions.append((Point(State_df.LongitudePresent[n], State_df.LatitudePresent[n])))
        ac_altitudes.append(Point(0,State_df.AltitudeBaroCorrected[n]))
        
        latlong_distances.append(Point(State_df.LongitudePresent[n], State_df.LatitudePresent[n]).distance(optimal_trajectory)*60)
        altitude_distances.append(Point(0,State_df.AltitudeBaroCorrected[n]).distance(optimal_altitudes))
    
    State_df['LatLongStateDistancesToTraj'] = latlong_distances
    State_df['AltStateDistancesToTraj'] = altitude_distances
    
    State_df.to_csv(os.path.join(outputPath,'DEVIATIONS_AopOwnshipStateDataRecord.csv'))

if __name__ == '__main__':
    RouteToStateDeviations(r'AopOwnshipStateDataRecord.csv',r'ROUTEALIGNED_AopOwnshipTrajectoryDataRecord.csv')

# -*- coding: utf-8 -*-
"""
Created on Fri Apr  2 13:44:56 2021

@author: Hari.rallapalli
"""
import xml.etree.ElementTree as ET
import re
import pandas as pd
import math

def unlist(lis):
    unlis = lis[0]
    return unlis

def TakeClosestGreater(number, collection):
    closest_greater_value = collection[collection > number].min()  
    return closest_greater_value

# filename = r'C:\Users\Hari.rallapalli\Desktop\APIJET\TAPEngine_MessagingLog_L_APIJET02_asteroid_20210303_165510.xml'
filename = r'C:\Users\Hari.rallapalli\Desktop\APIJET\TAPEngine_MessagingLog_L_APIJET02_asteroid_20210407_083056.xml'


with open(filename,'r', encoding='utf-8') as myFile:
    myFile=myFile.read()
    if "#" in myFile:
        myFile = re.sub(r'<#.+?#>', '', myFile)
    myFile = myFile + '</TapMessagingLog>'
 
root = ET.fromstring(myFile)

children = root.getchildren()

route_wall_time = []
route_data = []
route_waypoints = []
route_positions = []
route_altitude = []
route_first_position = []

state_wall_time = []
state_data = []
state_positions = []


for child in children:
    
    body = ET.tostring(child).decode()
    
    if "TAP_TAG" in body:
        UniqueID = re.search(r'value=".+?"',body).group(0)
        UniqueID = UniqueID.replace('"','')
        UniqueID = UniqueID.replace('value=','')
    
    if "OWNSHIP_STATE" in body:
        wall_time_body = re.search(r'wall_time=".+?"',body).group(0)
        wall_time_body =  wall_time_body.replace('"','')
        wall_time_body =  wall_time_body.replace('wall_time=','')        
        state_wall_time.append(wall_time_body)
        
        state_data_body = re.search(r'<OWNSHIP_STATE>.+?</OWNSHIP_STATE>',body).group(0)
        state_positions_data = re.findall('<POSITION.+?>', state_data_body)
        state_positions_data = re.findall("\d+\.\d+",unlist(state_positions_data))
        state_data.append(state_data_body)
        state_positions.append(state_positions_data)
        
    if "ROUTE_DATA" in body:
        wall_time_body = re.search(r'wall_time=".+?"',body).group(0)
        wall_time_body =  wall_time_body.replace('"','')
        wall_time_body =  wall_time_body.replace('wall_time=','')
        route_wall_time.append(wall_time_body)
        
        route_body = re.search(r'<ROUTE_DATA>.+?</ROUTE_DATA>',body).group(0)
        route_data.append(route_body)
        route_altitude_data = re.search('<CRUISE_ALTITUDE.+?>', route_body).group(0)
        route_waypoints_data = re.findall('<ROUTE_WAYPOINT.+?>', route_body)
        route_positions_data = re.findall('<POSITION.+?>', route_body)
        
        ### This is to drop Ownship projection to Trajectory
        route_waypoints_data = route_waypoints_data[1:]
        route_positions_data = route_positions_data[1:]
        ###
        
        route_first_position_data = route_positions_data[0]
        route_first_position_data = re.findall("\d+\.\d+",route_first_position_data)
        route_altitude.append(re.findall("\d+",route_altitude_data)[0])
        
        route_waypoints.append(route_waypoints_data)
        route_positions.append(unlist(route_positions_data))
        route_first_position.append(route_first_position_data)

s = {"UniqueID":UniqueID, "Wall_Time":state_wall_time, "State_Data":state_data, "State_Position":state_positions}
r = {"UniqueID":UniqueID, "Wall_Time":route_wall_time,"Route_Waypoints":route_waypoints,"Route_Positions":route_positions, "Route_First_Position":route_first_position, "Route_Altitude":route_altitude}

state_frame = pd.DataFrame(s)
route_frame = pd.DataFrame(r)

route_filtered = route_frame.drop_duplicates(subset = ["Route_Positions"])

closest_state_position = []
waypoints_check = []
altitude_check = []

for n in range(len(route_filtered)):
    
    state_closest_wall_time = TakeClosestGreater(route_filtered["Wall_Time"].iloc[n],state_frame["Wall_Time"])
    
    is_closest_state = state_frame['Wall_Time'] == state_closest_wall_time
    filtered_state = state_frame[is_closest_state]
    
    closest_state_position.append(filtered_state["State_Position"].iloc[0])
    try:
        cur_wpts = route_filtered["Route_Waypoints"].iloc[n]
        nex_wpts = route_filtered["Route_Waypoints"].iloc[n+1]
        waypoints_check.append(cur_wpts[1:] == nex_wpts)
        
        cur_alt = route_filtered["Route_Altitude"].iloc[n]
        nex_alt = route_filtered["Route_Altitude"].iloc[n+1]
        altitude_check.append(cur_alt == nex_alt)
        
    except:
        print("end of flightplan")
        waypoints_check.append(True)
        altitude_check.append(True)
        continue
    
route_filtered["Closest_State_Position"] = closest_state_position
route_filtered["Waypoints_Same"] = waypoints_check
route_filtered["Altitude_Same"] = altitude_check
   
distances = []
for n in range(len(route_filtered)):
    ### need to compute distances from next closest State point to waypoint
    
    p1 = route_filtered["Route_First_Position"].iloc[n]
    p2 = route_filtered["Closest_State_Position"].iloc[n]
    
    p1 = list(map(float, p1))
    p2 = list(map(float, p2))
    
    distance = math.sqrt( ((p1[0]-p2[0])**2)+((p1[1]-p2[1])**2) )
    
    ### assumption that one degree is equal to 60 nautical miles
    
    distance = distance*60
    
    distances.append(distance)
    
   
route_filtered["Route-to-State_Distance"] = distances

changed_flightplan = []
waypoint_hit_threshold = 50

for n in range(len(route_filtered)):
    
    if (route_filtered["Waypoints_Same"].iloc[n] == True and route_filtered["Altitude_Same"].iloc[n] == True and route_filtered["Route-to-State_Distance"].iloc[n] <= waypoint_hit_threshold):
        changed_flightplan.append(False)
    else:
        changed_flightplan.append(True)
        
route_filtered["Changed_Flightplan"] = changed_flightplan

# -*- coding: utf-8 -*-
"""
@author: Hari Rallapalli
"""


import pandas as pd
import io
import sys

def RouteParser():
    
    pathToFile = r'C:\Users\Hari.rallapalli\Desktop\APiJET\KCLKKMEM DAT\AopRouteDataRecord.csv'
    f = open(pathToFile)
    s = io.StringIO()
    header_info = None
    
    for ln in f:
        if not ln.strip():
                continue
        if ln.startswith('TAP'):
                header_info = ln.replace('\n',',',1)
                continue
        if ln.startswith('Source'):
                continue
        if ln.startswith('Type'):
            continue
        if ln.startswith('NAV'):
            ln = ln.replace('*','',1)
        if header_info == 0:
                print('NO valid route data found')
                sys.exit(1)
                
        s.write((header_info + ln))
    s.seek(0)
    # create new dataframe with desired column names
    
    
    colnames=['Source','SimTime','WallTime','Type','Symbol','Format','RouteFormat','WyptFormat','RestrictFormat','TurnPtFormat','RouteSource',\
            'RouteType','RouteCode','CruiseAltitude','CruiseAirspeed','CruiseMach','ClimbAirspeed','ClimbMach','DescentAirspeed','DescentMach','DescentFactor','CostIndex','NumWaypoints','RteChgType','Index',\
                'Unused','DataType','Latitude','Longitude','Altitude','ACMS','InboundTrueCourse','MagneticVariation','OutboundTrueCourse','GroundSpeed','Time','TypeAltitudeRestriction','UpperAltitudeRestriction','LowerAltitudeRestriction','SourceAltitudeRestriction','TypeAirspeedRestriction','UpperAirspeedRestriction','LowerAirspeedRestriction','SourceAirspeedRestriction','TypeMachRestriction','UpperMachRestriction','LowerMachRestriction','SourceMachRestriction','TypeTimeRestriction','UpperTimeRestriction','LowerTimeRestriction','SourceTimeRestriction','TrajectoryCode']
    
    
    df = pd.read_csv(s,  names=colnames)
    
    
    WAYPOINT_IDENTIFIER_ITERATOR = 0
    FLIGHTPLAN_START_TIME = df.loc[0,"SimTime"]
    
    APIJET_WAYPOINT_IDENTIFIER_ITERATOR = 0
    APIJET_FLIGHTPLAN_START_TIME = df.loc[0,"SimTime"]
    
    for Index in df["Index"].unique():
        is_IndexNum = df["Index"]==Index
        is_next_IndexNum = df["Index"]==Index+1
    
        df_IndexNum = df[is_IndexNum]
        df_next_IndexNum = df[is_next_IndexNum]
        
        # set_lat = set(df_IndexNum["Latitude"])
        # set_long = set(df_IndexNum["Longitude"])
        set_alt = set(df_IndexNum["CruiseAltitude"])
        set_waypoint = set(df_IndexNum["ACMS"])
        
        # set_next_lat = set(df_next_IndexNum["Latitude"])
        # set_next_long = set(df_next_IndexNum["Longitude"])
        set_next_alt = set(df_next_IndexNum["CruiseAltitude"])
        set_next_waypoint = set(df_next_IndexNum["ACMS"])
    
        # check_lat = set_lat - set_next_lat
        # check_long = set_long - set_next_long
        check_alt = set_alt - set_next_alt
        check_waypoint = set_waypoint - set_next_waypoint
        
        apijet_set_alt = set(df_IndexNum[1:]["CruiseAltitude"])
        apijet_set_next_alt = set(df_next_IndexNum[1:]["CruiseAltitude"])
        
        apijet_set_waypoint = set(df_IndexNum[1:]["ACMS"])
        apijet_set_next_waypoint = set(df_next_IndexNum[1:]["ACMS"])
    
        apijet_check_alt = apijet_set_alt - apijet_set_next_alt
        apijet_check_waypoint = apijet_set_waypoint - apijet_set_next_waypoint
                
        if len(check_waypoint)==0 and len(check_alt)==0:
                df.loc[is_IndexNum,"FLIGHTPLAN_WAYPOINT_IDENTIFIER"] = WAYPOINT_IDENTIFIER_ITERATOR
                df.loc[is_IndexNum,"FLIGHTPLAN_START_TIME"] = FLIGHTPLAN_START_TIME
                
        else:
            if set_next_waypoint.issubset(set_waypoint)==1 and len(check_alt)==0:
                df.loc[is_IndexNum,"FLIGHTPLAN_WAYPOINT_IDENTIFIER"] = WAYPOINT_IDENTIFIER_ITERATOR
                df.loc[is_IndexNum,"FLIGHTPLAN_START_TIME"] = FLIGHTPLAN_START_TIME
                
            else:
                WAYPOINT_IDENTIFIER_ITERATOR = WAYPOINT_IDENTIFIER_ITERATOR+1
                try:
                    FLIGHTPLAN_START_TIME = df_next_IndexNum["SimTime"].iloc[0]
                except:
                    df.loc[is_IndexNum,"FLIGHTPLAN_START_TIME"] = FLIGHTPLAN_START_TIME
                    pass
                
                df.loc[is_IndexNum,"FLIGHTPLAN_WAYPOINT_IDENTIFIER"] = WAYPOINT_IDENTIFIER_ITERATOR
                df.loc[is_IndexNum,"FLIGHTPLAN_START_TIME"] = FLIGHTPLAN_START_TIME
                
                
        if len(apijet_check_waypoint)==0 and len(apijet_check_alt)==0:
                df.loc[is_IndexNum,"APIJET_FLIGHTPLAN_WAYPOINT_IDENTIFIER"] = APIJET_WAYPOINT_IDENTIFIER_ITERATOR
                df.loc[is_IndexNum,"APIJET_FLIGHTPLAN_START_TIME"] = APIJET_FLIGHTPLAN_START_TIME
                
        else:
            if apijet_set_next_waypoint.issubset(apijet_set_waypoint)==1 and len(apijet_check_alt)==0:
                df.loc[is_IndexNum,"APIJET_FLIGHTPLAN_WAYPOINT_IDENTIFIER"] = APIJET_WAYPOINT_IDENTIFIER_ITERATOR
                df.loc[is_IndexNum,"APIJET_FLIGHTPLAN_START_TIME"] = APIJET_FLIGHTPLAN_START_TIME
                
            else:
                APIJET_WAYPOINT_IDENTIFIER_ITERATOR = APIJET_WAYPOINT_IDENTIFIER_ITERATOR+1
                try:
                    APIJET_FLIGHTPLAN_START_TIME = df_next_IndexNum["SimTime"].iloc[0]
                except:
                    df.loc[is_IndexNum,"APIJET_FLIGHTPLAN_START_TIME"] = APIJET_FLIGHTPLAN_START_TIME
                    pass
                
                df.loc[is_IndexNum,"APIJET_FLIGHTPLAN_WAYPOINT_IDENTIFIER"] = APIJET_WAYPOINT_IDENTIFIER_ITERATOR
                df.loc[is_IndexNum,"APIJET_FLIGHTPLAN_START_TIME"] = APIJET_FLIGHTPLAN_START_TIME
                
    
                
    return(df)

if __name__ == '__main__':
    RouteDf = RouteParser()
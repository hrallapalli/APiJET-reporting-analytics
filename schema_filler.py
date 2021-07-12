# -*- coding: utf-8 -*-
"""
@author: Hari.rallapalli
"""
import pandas as pd
import os
import datetime

base_path = r'/Users/vinh.bui/Desktop/Hari_Example'

""" Asha's suggestions for next update

1. Rename the output_file.csv to another name rather than Schema... -- Done 

2. Advisory ID 127 from BUR-SEA listed twice 

3. Add title to 1st column (ex: Reco Count)

4. Change "Tail ID" to "Device ID" -- Done 

5. Extract the actually recommendations displayed to Pilot into the same output CSV or a seperate CSV

6. Add counter to the number of flights we are tracking 

7. What does SAVINGS_OptimalSaving.csv represent?




"""


# messagelog_folder = r'messagelog_0'

messagelog_folder = r'analysis_1625335908'

# datatranslator_folder = r'analysis_1625625045287'

datatranslator_folder = r'analysis_1625335908'


messagelog_path = os.path.join(base_path,messagelog_folder)
datanalysis_path = os.path.join(base_path,datatranslator_folder)

constraints_frame = pd.read_csv(os.path.join(messagelog_path, 'CONSTRAINTS_Frame.csv'))
taptag_frame = pd.read_csv(os.path.join(messagelog_path, 'TAP_TAG_Frame.csv'))
aircrafttype_frame = pd.read_csv(os.path.join(messagelog_path, 'AIRCRAFT_TYPE_Frame.csv'))
advisoryselectrequest_frame = pd.read_csv(os.path.join(messagelog_path, 'ADVISORY_SELECT_REQUEST_Frame.csv'))
event_frame = pd.read_csv(os.path.join(messagelog_path, 'EVENT_Frame.csv'))
moderequest_frame = pd.read_csv(os.path.join(messagelog_path, 'MODE_REQUEST_Frame.csv'))
SAVINGS_refresh_frame = pd.read_csv(os.path.join(datanalysis_path, 'SAVINGS_TapAdvisoryRefreshRecord.csv'))


AIRLINE = 'Alaska Airlines'
FLIGHT_NUMBER = constraints_frame['value'][constraints_frame['message_tag']=='FLIGHT_NUMBER'].iloc[0]
AIRCRAFT_TYPE = aircrafttype_frame['value'].iloc[0]
TAIL_ID = taptag_frame['value'].iloc[0]
ORIGIN = constraints_frame['value'][constraints_frame['message_tag']=='ORIGIN'].iloc[0]
DESTINATION = constraints_frame['value'][constraints_frame['message_tag']=='DESTINATION'].iloc[0]
DATETIME = float(taptag_frame['message_time'].iloc[0])
DATETIME = datetime.datetime.fromtimestamp(DATETIME).strftime('%Y-%m-%d %H:%M:%S')
INITAL_CRUISE_ALTITUDE = constraints_frame['value'][constraints_frame['message_tag']=='CRUISE_ALTITUDE'].iloc[0]

RECOMMNEDATION_DISPLAY = 'where can we get this name?'


advisoriesselected = advisoryselectrequest_frame[advisoryselectrequest_frame["advisory_id"] != -1]


ADVISORY_ID = advisoriesselected['advisory_id'].to_list()

ADVISORY_TYPE = []
FUEL_SAVINGS = []
TIME_SAVINGS = []
TRIPCOST_SAVINGS = []
WAYPOINT_1 = []
WAYPOINT_2 = []
FLIGHT_LEVEL = []
RECONNECT_WAYPOINT = []

for aid in ADVISORY_ID:
    ADVISORY_TYPE.append(SAVINGS_refresh_frame['AdvisoryType'][SAVINGS_refresh_frame['AdvisoryId']==aid].iloc[0])
    FUEL_SAVINGS.append(SAVINGS_refresh_frame['FuelOutcome'][SAVINGS_refresh_frame['AdvisoryId']==aid].iloc[0])
    TIME_SAVINGS.append(SAVINGS_refresh_frame['TimeOutcome'][SAVINGS_refresh_frame['AdvisoryId']==aid].iloc[0])
    TRIPCOST_SAVINGS.append(SAVINGS_refresh_frame['TripCostOutcome'][SAVINGS_refresh_frame['AdvisoryId']==aid].iloc[0])
    WAYPOINT_1.append(SAVINGS_refresh_frame['WP1'][SAVINGS_refresh_frame['AdvisoryId']==aid].iloc[0])
    WAYPOINT_2.append(SAVINGS_refresh_frame['WP2'][SAVINGS_refresh_frame['AdvisoryId']==aid].iloc[0])
    FLIGHT_LEVEL.append(SAVINGS_refresh_frame['FlightLevel'][SAVINGS_refresh_frame['AdvisoryId']==aid].iloc[0])
    RECONNECT_WAYPOINT.append(SAVINGS_refresh_frame['Reconnect'][SAVINGS_refresh_frame['AdvisoryId']==aid].iloc[0])

SELECTED_DATETIME = []
for dt in advisoriesselected['message_time'].to_list(): 
    SELECTED_DATETIME.append(datetime.datetime.fromtimestamp(dt).strftime('%Y-%m-%d %H:%M:%S'))
    
ATC_ACCEPT_TIME = []
for accept_t in event_frame['message_time'][event_frame['act']=='ATCApproved'].to_list():
    ATC_ACCEPT_TIME.append(datetime.datetime.fromtimestamp(accept_t).strftime('%Y-%m-%d %H:%M:%S'))

ATC_REJECT_TIME = []
for reject_t in event_frame['message_time'][event_frame['act']=='ATCRejected'].to_list():
    ATC_REJECT_TIME.append(datetime.datetime.fromtimestamp(reject_t).strftime('%Y-%m-%d %H:%M:%S'))

MODE = moderequest_frame['mode'].iloc[0]


s = {'AIRLINE':AIRLINE,
     'FLIGHT_NUMBER':FLIGHT_NUMBER,
     'AIRCRAFT_TYPE':AIRCRAFT_TYPE,
     'Device ID':TAIL_ID,
     'ORIGIN':ORIGIN,
     'DESTINATION':DESTINATION,
     'DATETIME':DATETIME,
     'INITAL_CRUISE_ALTITUDE':INITAL_CRUISE_ALTITUDE,
     'ADVISORY_TYPE':ADVISORY_TYPE,
     'ADVISORY_ID':ADVISORY_ID,
     'FUEL_SAVINGS':FUEL_SAVINGS,
     'TIME_SAVINGS':TIME_SAVINGS,
     'TRIPCOST_SAVINGS':TRIPCOST_SAVINGS,
     'WAYPOINT_1':WAYPOINT_1,
     'WAYPOINT_2':WAYPOINT_2,
     'FLIGHT_LEVEL':FLIGHT_LEVEL,
     'RECONNECT_WAYPOINT':RECONNECT_WAYPOINT,
     'SELECTED_DATETIME':SELECTED_DATETIME,
     'ATC_ACCEPT_TIME':ATC_ACCEPT_TIME,
     'ATC_REJECT_TIME':ATC_REJECT_TIME,
     'MODE':MODE}

schema = pd.DataFrame(dict([ (k,pd.Series(v)) for k,v in s.items() ]))
#Change Output file name
schema.to_csv(os.path.join(base_path,'DW_Recommendation_Record.csv')) 

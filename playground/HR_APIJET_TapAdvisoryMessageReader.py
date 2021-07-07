# -*- coding: utf-8 -*-
"""
Created on Mon May 17 09:17:46 2021

@author: Hari.rallapalli
"""
import xml.etree.ElementTree as ET
import re
import pandas as pd
import os

base_path = r'C:\Users\Hari.rallapalli\OneDrive - APiJET\Desktop\APIJET\20210706_test\flights\1'

analysis_path = r'C:\Users\Hari.rallapalli\OneDrive - APiJET\Desktop\APIJET\20210706_test\flights\1\analysis_1625625045287'

# for file in os.listdir(base_path):
#     if file.endswith(".xml"):
#         filename = os.path.join(base_path,file)
        
filename = r'C:\Users\Hari.rallapalli\OneDrive - APiJET\Desktop\APIJET\20210706_test\flights\1\TAPEngine_MessagingLog_R_Walters-2cf0-EFB_BB45_20210703_022017.xml'
        
with open(filename,'r', encoding='utf-8') as myFile:
    myFile=myFile.read()
    if "#" in myFile:
        # myFile = re.sub(r'<#.+?#>', '<Go command="You dont need this right now" />', myFile)
        myFile = re.sub(r'<#.+?#>', '', myFile)
    if '</TapMessagingLog>' not in myFile:
        myFile = myFile + '</TapMessagingLog>'
 
root = ET.fromstring(myFile)

tree = ET.ElementTree(root)

cur_time = []
cur_type = []

message_type =[]
message_time = []
message_tag = []
message_level = []
message_text = []

def traverse(elem, level=0):
    yield elem, level

    for child in elem:
        yield from traverse(child, level + 1)
        

# Replace NaN by empty dict
def replace_nans_with_dict(series):
    for idx in series[series.isnull()].index:
        series.at[idx] = {}
    return series



# Explodes list and dicts
def df_explosion(df, col_name:str):

    if df[col_name].isna().any():
        df[col_name] = replace_nans_with_dict(df[col_name])

    df.reset_index(drop=True, inplace=True)

    df1 = pd.DataFrame(df.loc[:,col_name].values.tolist())

    df = pd.concat([df,df1], axis=1)

    df.drop([col_name], axis=1, inplace=True)

    return df

for elem, level in traverse(root):
    # print("  " * level + elem.tag)
    
    if elem.tag == 'TapMessage':
        cur_time = float(elem.attrib.get('wall_time'))
        
    elif elem.tag == 'Body':
        continue
    
    elif elem.tag == 'TapMessagingLog':
        continue
    
    elif level == 3:
        cur_type = elem.tag
        message_type.append(cur_type)
        message_time.append(cur_time)
        message_tag.append(elem.tag)
        message_level.append(level)
        message_text.append(elem.attrib)
        
    else:
        message_type.append(cur_type)
        message_time.append(cur_time)
        message_tag.append(elem.tag)
        message_level.append(level)
        message_text.append(elem.attrib)
    # print("  " * level + str(elem.attrib))

MessageFrame = pd.DataFrame([message_time,message_type,message_tag,message_level,message_text]).T
MessageFrame = MessageFrame.rename(columns={0:'message_time',1:'message_type',2:'message_tag',3:'message_level',4:'message_text'})

del(message_time,message_type,message_tag,message_level,message_text)

for n, typ in enumerate(MessageFrame['message_type'].unique()):
    tmpFrame = MessageFrame[MessageFrame['message_type']==str(typ)]
    tmpFrame = df_explosion(tmpFrame, 'message_text')
    
    tmpFrame.to_csv(os.path.join(analysis_path,str(typ) + '_Frame.csv'))
    

# attrib_moderequest = []

# attrib_UID = []

# attrib_wall_time = []
# attrib_advisory_time = []
# attrib_update = []
# attrib_advisory = []
# attrib_wpt1 = []
# attrib_wpt2 = []
# attrib_rejoin = []
# attrib_endpoint = []
# attrib_outcome = []
# attrib_flightlevel = [] 

# event_UID = []
# event_time = []
# event_event = []
# event_info = []
# event_mode = []
# event_reason = []


# for message in tree.iterfind('TapMessage'):
#     time = float(message.attrib['wall_time'])
    
#     try:
#         if message[0][0].tag == 'MODE_REQUEST':
#             mode_request = message[0][0].attrib
#     except:
#         continue
    
#     if message[0][0].tag == 'TAP_TAG':
#         UID = message[0][0].attrib    

#     if message[0][0].tag == 'UPDATE':
#         TAP_UPDATE = message[0][0].attrib
#         attrib_wall_time.append(time)
#         attrib_update.append(TAP_UPDATE)
        
#         for n,advisory in enumerate(message[0][0]):
#             attrib_advisory_time.append(time)
#             attrib_advisory.append(advisory.attrib)
            
#             attrib_wpt1.append(advisory[0][0].attrib)
#             attrib_wpt2.append(advisory[0][1].attrib)
            
#             attrib_rejoin.append(advisory[0][2].attrib)
#             attrib_endpoint.append(advisory[0][0][0].attrib)
            
#             attrib_moderequest.append(mode_request)
        
#             attrib_UID.append(UID)
            
#             if message[0][0][n][1].tag == "OUTCOME":
#                 attrib_outcome.append(message[0][0][n][1].attrib)
#             else:
#                 attrib_outcome.append({'type': 'NA', 'value': 'NA', 'units': 'NA'})
                
#             if advisory[0][3].tag == 'FLIGHT_LEVEL':
#                 attrib_flightlevel.append(advisory[0][3].attrib)
#             else:
#                 attrib_flightlevel.append({'value': 'NA'})
                
                
#     if message[0][0].tag == 'EVENT':
#         event_time.append(time)
#         event_event.append(message[0][0].attrib)
#         event_UID.append(UID)
        
#         try:
        
#             if message[0][0][0].tag == "INFO":
#                event_info.append(message[0][0][0].attrib)
                
#             if message[0][0][1].tag == "MODE":
#                event_mode.append(message[0][0][1].attrib)                
                
#             if message[0][0][2].tag == "REASON":
#                event_reason.append(message[0][0][2].attrib)
                
                
#         except:
            
#             event_info.append({"evaluate_id":"NA", "nadvisories":"NA", "config_index":"NA"})
#             event_mode.append({"value":"NA"})
#             event_reason.append({"value":"Other"})
#             continue
        
#     if message[0][0].tag == 'CONSTRAINTS':
#         print(message[0][0].tag)
            
                
            

# attrib_UID = pd.DataFrame(attrib_UID)
# attrib_UID = attrib_UID.rename(columns = {"value": "UID"})

# attrib_moderequest = pd.DataFrame(attrib_moderequest)
# attrib_moderequest = attrib_moderequest.rename(columns = {"mode": "RequestMode"})
        
        
# attrib_advisory_time = pd.DataFrame(attrib_advisory_time)
# attrib_advisory_time = attrib_advisory_time.rename(columns = {0:"WallTime"})

# attrib_update = pd.DataFrame(attrib_update)

# attrib_advisory = pd.DataFrame(attrib_advisory)

# attrib_wpt1 = pd.DataFrame(attrib_wpt1)
# attrib_wpt1 = attrib_wpt1.rename(columns = {"type":"WPT_1_type", "name":"WPT_1_name"})

# attrib_wpt2 = pd.DataFrame(attrib_wpt2)
# attrib_wpt2 = attrib_wpt2.rename(columns = {"type":"WPT_2_type", "name":"WPT_2_name"})

# attrib_rejoin = pd.DataFrame(attrib_rejoin)
# attrib_rejoin = attrib_rejoin.rename(columns = {"type":"RejoinType", "name":"RejoinWaypoint"})

# attrib_endpoint = pd.DataFrame(attrib_endpoint)
# attrib_endpoint = attrib_endpoint.rename(columns = {"lat":"EndpointLat", "lon":"EndpointLon"})

# attrib_outcome = pd.DataFrame(attrib_outcome)
# attrib_outcome = attrib_outcome.rename(columns = {"type" : "SavingType", "value" : "SavingsValue", "units" : "SavingsUnits"})

# attrib_flightlevel = pd.DataFrame(attrib_flightlevel)
# attrib_flightlevel = attrib_flightlevel.rename(columns = {"value" : "FlightLevel"})
       
# AdvisoryFrame = pd.concat([attrib_UID, attrib_moderequest, attrib_advisory_time, attrib_advisory, attrib_wpt1, attrib_wpt2, attrib_rejoin, attrib_endpoint, attrib_outcome, attrib_flightlevel], axis = 1)
# AdvisoryFrame.to_csv(os.path.join(base_path,"AdvisoryFrame.csv"))


# event_UID = pd.DataFrame(event_UID)
# event_UID = event_UID.rename(columns={"value":"UID"})

# event_time = pd.DataFrame(event_time)
# event_time = event_time.rename(columns={0:"WallTime"})

# event_event = pd.DataFrame(event_event)
# event_info = pd.DataFrame(event_info)

# event_mode = pd.DataFrame(event_mode)
# event_mode = event_mode.rename(columns={"value":"mode"})

# event_reason = pd.DataFrame(event_reason)
# event_reason = event_reason.rename(columns={"value":"reason"})

# EventFrame = pd.concat([event_UID, event_time, event_event, event_info, event_mode, event_reason], axis = 1)
# EventFrame.to_csv(os.path.join(base_path,"EventFrame.csv"))
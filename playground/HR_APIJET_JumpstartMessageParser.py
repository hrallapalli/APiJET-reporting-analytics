# -*- coding: utf-8 -*-

import datetime as dt
import pandas as pd
import re

def find_inner(s):
    temp = s.partition('{')[-1].rpartition('}')[0]
    if not temp:
        return s

    return find_inner(temp)

def message_splitter(message):
    
    key = []
    val = []
    
    split_message = re.split(',', message)
    
    for ele in split_message:
        try:
            keyval = re.split(':', ele)
            
            keyval[0] = keyval[0].replace('"', "")
            key.append(keyval[0])
            val.append(keyval[1])
        
        except:
            print('Something is screwy with these messages... there are more values than columns!! Are you sure these are jumpstart route messages???')
    
    return key, val
        
        
    
js_log_filename = r'C:\Users\Hari.rallapalli\Desktop\APIJET\jumpstart_logs_sample.txt'

js_full = open(js_log_filename,"r")

js_message_frame = pd.DataFrame(columns = ['Timestamp', 'Message'])

for n, line in enumerate(js_full):
    
    # date and time information to UTC timestamp. I have to make an assumption that the year is this year... can we please add a year to jumpstart messages?
    date_time_str = line[0:15] # <---- it is really unfortunate that I have to hard code character counts to get a datetime string...
    todays_date = dt.date.today()
    date_time_str = str(todays_date.year) + ' ' + date_time_str
    
    date_time_obj = dt.datetime.strptime(date_time_str, '%Y %b %d %H:%M:%S')
    date_time_stamp = dt.datetime.timestamp(date_time_obj)

    # pull message information and store in a useful dataframe for reference
    
    line_message = find_inner(line)
    js_message_frame = js_message_frame.append({'Timestamp': date_time_stamp, 'Message' : line_message}, ignore_index = True)
    
    # I need to skip PROPOSED route messages, and messages when the aircraft is still on the ground. Thankfully, the "etd" message parameter is only printed when the aircraft is on the ground.
    # It makes sense that the estimated time of departure is no longer relevant after the aircraft takes off!!
    
    if "PROPOSED" in line:
        continue
    elif "etd" in line:
        continue
    
    # Then, I can parse the route messages and massage them into pandas dataframe columns
    
    keys, vals = message_splitter(line_message)
    
    if 'js_route_frame' not in locals():
        colnames = ["Timestamp"] + keys
        js_route_frame = pd.DataFrame(columns = colnames)
        
    to_append = [date_time_stamp] + vals
    a_series = pd. Series(to_append, index = js_route_frame.columns)
    js_route_frame = js_route_frame. append(a_series, ignore_index=True)
    
    # Then, I filter the "route_data" column for only unique routes
    
    filtered_route_frame = js_route_frame.drop_duplicates(subset = ["raw_route"])
    
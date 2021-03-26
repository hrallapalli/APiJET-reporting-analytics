# -*- coding: utf-8 -*-
"""
@author: Hari Rallapalli
"""
import pandas as pd
import io
import sys

def TrajParser():

    pathToFile = r'C:\Users\Hari.rallapalli\Desktop\APiJET\KCLKKMEM DAT\AopOwnshipTrajectoryDataRecord.csv'
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
            colnames_1 = ln.replace('Type','CsvType',1).replace('\n',',',1)
            continue
        if ln.startswith('Timestamp'):
            colnames_2 = ln.replace('\n',',',1)
            continue
        if header_info == 0:
                print('NO valid Trajectory data found')
                sys.exit(1)
                
        s.write((header_info + ln))
    s.seek(0)
    
    colnames = (colnames_1[:-1] + ',' + colnames_2[:-2])
    
    df = pd.read_csv(s, names = colnames.split(','))
    
    return(df)

if __name__ == '__main__':
    TrajDf = TrajParser()
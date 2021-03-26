# -*- coding: utf-8 -*-
"""
@author: Hari.rallapalli
"""
import pandas as pd
import io
import sys

def StateParser():

    pathToFile = r'C:\Users\Hari.rallapalli\Desktop\APiJET\KCLKKMEM DAT\AopOwnshipStateDataRecord.csv'
    f = open(pathToFile)
    s = io.StringIO()
    header_info = None
    
    for ln in f:
        if not ln.strip():
            continue
        if ln.startswith('Source'):
            colnames = ln.replace('Type','CsvType',1).replace('\n',',',1)
            continue
        if header_info == 0:
                print('NO valid Trajectory data found')
                sys.exit(1)
                
        s.write(ln)
    s.seek(0)
    
    df = pd.read_csv(s, names = colnames.split(','))
    
    return(df)

if __name__ == 'main':
    StateDf = StateParser()

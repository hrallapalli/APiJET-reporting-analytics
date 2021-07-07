# -*- coding: utf-8 -*-
"""
Created on Mon May  3 13:13:36 2021

@author: -
"""

import pandas as pd
import io
import sys
import os
import matplotlib.pyplot as plt
import seaborn as sns


def TapAdvisoryParser(pathToAdvisory, outputPath):

    # pathToFile = r'C:\Users\Hari.rallapalli\OneDrive - APiJET\Desktop\APIJET\20210423_test\Flight_Run_0\Flight_Run_0_TapAdvisoryRefreshDataRecord.csv'
    # outputPath = r'C:\Users\Hari.rallapalli\OneDrive - APiJET\Desktop\APIJET\20210423_test\Flight_Run_0\analysis_1619201197326'
    f = open(pathToAdvisory)
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
        if ln.startswith('AdvisoryId'):
            colnames_2 = ln.replace('\n',',',1)
            continue
        if header_info == 0:
                print('NO valid Trajectory data found')
                sys.exit(1)
                
        s.write((header_info + ln))
    s.seek(0)
    
    colnames = (colnames_1[:-1] + ',' + colnames_2[:-2])
    
    df = pd.read_csv(s, names = colnames.split(','))
    
    optimal_savings = df.loc[df['TripCostOutcome'] == df['TripCostOutcome'].min()]
    
    df.to_csv(os.path.join(outputPath,'SAVINGS_TapAdvisoryRefreshRecord.csv'))
    optimal_savings.to_csv(os.path.join(outputPath,'SAVINGS_OptimalSavings.csv'))
    
    plt.figure()
    plt.title('Trip Cost Savings (Dollars)\nLateral = red, Vertical = blue, Combo = green')
    sns.lmplot(x='SimTime',y='TripCostOutcome', data=df, hue='AdvisoryType', fit_reg=False, scatter_kws={"s": 1})
    plt.savefig(os.path.join(outputPath,'TripCostSavings.png'), dpi = 300)
    plt.close('all')
    

    return(df)

if __name__ == '__main__':

    TapAdvisoryFrame = TapAdvisoryParser(r'C:\Users\Hari.rallapalli\OneDrive - APiJET\Desktop\APIJET\20210603_test\Flight_Run_0\Flight_Run_0_TapAdvisoryRefreshDataRecord.csv', r'C:\Users\Hari.rallapalli\OneDrive - APiJET\Desktop\APIJET\20210608_test\Flight_Run_0\analysis_1619201197326')
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  4 09:15:48 2017

@author: Steve
"""

import os
import pandas


def getData( dataDirectory):
    os.chdir(dataDirectory)

    fileList = os.listdir(dataDirectory)



    varList = ['stim.1','prompt.1','answer.1','trials.thisRepN',
           'trials.thisTrialN','trials.thisIndex','participant',
           'Trials_response.keys','Trials_response.corr','Trials_response.rt']

    varListFixed = ['stim1','prompt1','answer1','trialsthisRepN',
           'trialsthisTrialN','trialsthisIndex','participant',
           'Trials_responsekeys','Trials_responsecorr','Trials_responsert']

    #initialize master DF
    master = pandas.DataFrame()

    for file in fileList:
        data = pandas.read_csv(file,skipinitialspace=True)
        data = data[varList]
        data.columns = varListFixed
        data = data[data['trialsthisTrialN'] > -1]
        master = master.append(data)
    
    
    return master;


frizData = getData('C:\\Users\\Steve\\Documents\\Dropbox\\Penn Post Doc\\Frisbee_Ref_Frames\\data\\batch1\\friz_clean')
    
navData = getData('C:\\Users\\Steve\\Documents\\Dropbox\\Penn Post Doc\\Frisbee_Ref_Frames\\data\\batch1\\nav_clean')


# -*- coding: utf-8 -*-
"""
Created on Mon Dec  4 09:15:48 2017

@author: Steve
"""
# <codecell>.
import os
import pandas
import numpy as np

def getData(dataDirectory):
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
        participant_name = file.split('_')[0]
        data.participant = np.repeat(participant_name,len(data.participant))
        master = master.append(data)
        
    
    
    return master #fileList; for debugging below



# <codecell>
"""
#debug making sure all participant names/numbers match


friz,frizFiles= getData('C:\\Users\\stweis\\Dropbox\\Penn Post Doc\\Frisbee_Ref_Frames\\data\\batch1\\friz_clean')
nav,navFiles= getData('C:\\Users\\stweis\\Dropbox\\Penn Post Doc\\Frisbee_Ref_Frames\\data\\batch1\\nav_clean')


matches = []
navFiles_names = []
frizFiles_names = []
navFiles.sort()
frizFiles.sort()

for i in range(58):
    frizFiles_names.append(frizFiles[i].split('_')[0])
    navFiles_names.append(navFiles[i].split('_')[0])

    if frizFiles_names[i] == navFiles_names[i]:
        matches.append(True)
    else:
        matches.append(False)
"""             
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  4 13:39:33 2017

@author: Steve
"""


# <codecell>

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from importData import getData
import statsmodels.api as sm
import statsmodels.formula.api as smf
frizData = getData('C:\\Users\\Steve\\Documents\\Dropbox\\Penn Post Doc\\Frisbee_Ref_Frames\\data\\batch1\\friz_clean')
    
navData = getData('C:\\Users\\Steve\\Documents\\Dropbox\\Penn Post Doc\\Frisbee_Ref_Frames\\data\\batch1\\nav_clean')

# <codecell>

def removeHighRTs(dv,data):
    rtThresh = 4*np.std(data[dv])
    rtMean = np.mean(data[dv])
    dataThresh = data.loc[data[dv] < (rtMean + rtThresh)]
    dataThresh = dataThresh.loc[dataThresh[dv] > 0]
    return dataThresh

def removeWrongAnswers(dv,data):
    dataCorrect = data.loc[data[dv] == 1]
    return dataCorrect

frizDataThresh = removeHighRTs('Trials_responsert',frizData)
navDataThresh = removeHighRTs('Trials_responsert',navData)

data = frizDataThresh.append(navDataThresh)
data = removeWrongAnswers('Trials_responsecorr',data)

unthreshed_data = frizData.append(navData)
# <codecell>
sns.boxplot(x='prompt1',y='Trials_responsert',data=data)
plt.show()

# <codecell>

factor_order = ['The force is away.','The force is home.','The force is backhand.','The force is forehand.',
'Go away. ','Go home.','Go left. ','Go right. ']

ax = sns.factorplot(x = "prompt1", y = "Trials_responsert", data = data, hue = "stim1", palette=['red','green','blue','yellow'], 
                    kind = "point", size = 8, order=factor_order,col='answer1')

# <codecell>
factor_order = ['The force is away.','The force is home.','The force is backhand.','The force is forehand.',
'Go away. ','Go home.','Go left. ','Go right. ']

ax = sns.factorplot(x = "prompt1", y = "Trials_responsert", data = unthreshed_data, hue = "stim1", palette=['red','green','blue','yellow'], 
                    kind = "point", size = 8, order=factor_order,col='Trials_responsecorr')

# <codecell>






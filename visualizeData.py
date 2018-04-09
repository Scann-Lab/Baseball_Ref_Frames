# -*- coding: utf-8 -*-
"""
Created on Mon Dec  4 13:39:33 2017

@author: Steve
"""


# <codecell>

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import scipy
import statsmodels.api as sm
#import statsmodels.formula.api as smf

#custom function
from importData import getData

#Get Data
frizData = getData('C:\\Users\\stweis\\Dropbox\\Penn Post Doc\\Frisbee_Ref_Frames\\data\\batch1\\friz_clean')
    
navData = getData('C:\\Users\\stweis\\Dropbox\\Penn Post Doc\\Frisbee_Ref_Frames\\data\\batch1\\nav_clean')

additionalData = pd.read_excel('C:\\Users\\stweis\\Dropbox\\Penn Post Doc\\Frisbee_Ref_Frames\\data\\batch1\\additionalData_For_Python.xlsx',header=0)
additionalData['participant'] = additionalData['psychopycode']

#Clean data functions
def removeHighRTs(dv,data):
    rtThresh = 2*np.std(data[dv])
    rtMean = np.mean(data[dv])
    dataThresh = data.loc[data[dv] < (rtMean + rtThresh)]
    dataThresh = dataThresh.loc[dataThresh[dv] > 0]
    return dataThresh

def removeWrongAnswers(dv,data):
    dataCorrect = data.loc[data[dv] == 1]
    return dataCorrect



def renameFactorLevels(data,friz_or_nav):
        
    data['condition'] = friz_or_nav
    prompts = sorted(data.prompt1.unique())
    stims = sorted(data.stim1.unique())
    new_stims = ['far_left','far_right','near_left','near_right']

    if friz_or_nav == 'friz':    
        new_prompts = ['Away','Left','Right','Home']
    else:
        new_prompts = ['Away','Home','Left','Right']


    for i in range(len(prompts)):
        data = data.replace(prompts[i],new_prompts[i])
        data = data.replace(stims[i],new_stims[i])
        
    return data


def newFactorPrompts(row):
    if row['prompt1'] == 'Home' or row['prompt1'] == 'Away':
        return 'Absolute'
    else:
        return 'Relative'
    
def newFactorStims(row):
    if row['stim1'] == 'near_right' or row['stim1'] == 'near_left':
        return 'Near'
    else:
        return 'Far'
    


#Clean data
frizData = renameFactorLevels(frizData,'Frisbee')
navData = renameFactorLevels(navData,'Navigation')

frizData['stimLoc'] = frizData.apply(lambda row: newFactorStims(row),axis=1)
navData['stimLoc'] = navData.apply(lambda row: newFactorStims(row),axis=1)

frizData['promptType'] = frizData.apply(lambda row: newFactorPrompts(row),axis=1)
navData['promptType'] = navData.apply(lambda row: newFactorPrompts(row),axis=1)


frizDataThresh = removeHighRTs('Trials_responsert',frizData)
navDataThresh = removeHighRTs('Trials_responsert',navData)

all_answers_data = frizDataThresh.append(navDataThresh)
data = removeWrongAnswers('Trials_responsecorr',all_answers_data)

unthreshed_data = frizData.append(navData)

neccessaryAdditionalData = additionalData.loc[:,
                                              ["Sex","participant",
                                               "SBSOD_AVERAGE",
                                               "Friz_Total_Years_Played",
                                               "Friz_Force_Preference",
                                               "Friz_Position"]]






#data.to_csv('C:\\Users\\stweis\\Documents\\Github\\Ultimate\\data_for_R.csv')

# <codecell>

#recreate All Figures with either thresholded or unthresholded Data

dataForPlot = all_answers_data


# pivots data for plotting

pivoted = dataForPlot.pivot_table(index='participant',columns=['condition','stimLoc','promptType'],values='Trials_responsert',aggfunc=np.mean)

pivoted['Frisbee_Rel_minus_Abs_Far'] = pivoted['Frisbee']['Far']['Relative'] - pivoted['Frisbee']['Far']['Absolute']
pivoted['Frisbee_Rel_minus_Abs_Near'] = pivoted['Frisbee']['Near']['Relative'] - pivoted['Frisbee']['Near']['Absolute']
pivoted['Frisbee_Rel_minus_Abs'] = (pivoted['Frisbee_Rel_minus_Abs_Far'] + pivoted['Frisbee_Rel_minus_Abs_Near'])/2
pivoted['Nav_Rel_minus_Abs_Far'] = pivoted['Navigation']['Far']['Relative'] - pivoted['Navigation']['Far']['Absolute']
pivoted['Nav_Rel_minus_Abs_Near'] = pivoted['Navigation']['Near']['Relative'] - pivoted['Navigation']['Near']['Absolute']
pivoted['Nav_Rel_minus_Abs'] = (pivoted['Nav_Rel_minus_Abs_Far'] + pivoted['Nav_Rel_minus_Abs_Near'])/2

pivotedAllFour = dataForPlot.pivot_table(index='participant',columns=['condition','prompt1'],values='Trials_responsert',aggfunc=np.mean)
pivotedAllFour['Friz_Back_minus_Fore'] = pivotedAllFour['Frisbee']['Left'] - pivotedAllFour['Frisbee']['Right']
pivotedAllFour['Friz_Home_minus_Away'] = pivotedAllFour['Frisbee']['Home'] - pivotedAllFour['Frisbee']['Away']
pivotedAllFour['Nav_Left_minus_Right'] = pivotedAllFour['Navigation']['Left'] - pivotedAllFour['Navigation']['Right']
pivotedAllFour['Nav_Home_minus_Away'] = pivotedAllFour['Navigation']['Home'] - pivotedAllFour['Navigation']['Away']
pivoted.sort_index(inplace=True)
pivotedAllFour.sort_index(inplace=True)

# Merges pivoted data with additional data (columns from necessaryAdditionalData)
grandmean = dataForPlot.pivot_table(index='participant',columns=['condition'],values='Trials_responsert',aggfunc=np.mean)
pivoted['participant'] = pivoted.index
pivoted[['participant']] = pivoted[['participant']].apply(pd.to_numeric)
neccessaryAdditionalData.sort_values('participant',inplace=True)
pivoted.sort_values('participant',inplace=True)
merged = pivoted.merge(neccessaryAdditionalData,on='participant')
grandmean['participant'] = grandmean.index
grandmean[['participant']] = grandmean[['participant']].apply(pd.to_numeric)

merged = merged.merge(grandmean,on='participant')




# <codecell> 

nonaPivoted = pivoted.dropna()
ax1 = sns.distplot(nonaPivoted['Nav_Rel_minus_Abs'],label='Navigation')
sns.distplot(nonaPivoted['Frisbee_Rel_minus_Abs'],label='Frisbee')
ax1.set(xlabel='Difference between Relative and Absolute Prompts',ylabel='Frequency')
plt.legend()
plt.show()

# <codecell>
# Line Graphs
sns.set_style('ticks')
sns.set_context('talk')
ax1 = sns.factorplot(x = "promptType", y = "Trials_responsert", data = dataForPlot, hue = "stimLoc",palette=['red','blue'], 
                     kind = "point", size = 8,col='condition')
ax1.set(xlabel='Prompt Label', ylabel='Response Time (s)')
ax1.set_titles("{col_name} Condition")

ax2 = sns.factorplot(x = "prompt1", y = "Trials_responsert", data = dataForPlot, hue = "stim1", palette=['red','salmon','blue','dodgerblue'],
                    kind = "point", size = 8,col='condition', order=['Right','Left','Away','Home'], hue_order=['near_right','near_left','far_right','far_left'])

ax2.set(xlabel='Prompt Label', ylabel='Response Time (s)')
ax2.set_titles("{col_name} Condition")




# <codecell>
# Joint Plots with and without outliers (generated below)
# Outliers calculated on answers_all_data
ax1 = sns.jointplot(pivoted['Frisbee_Rel_minus_Abs_Near'], pivoted['Frisbee_Rel_minus_Abs_Far'], kind="reg")

outliersFriz = ['44376975','99990726','26044874','52817250']
noOutliersFriz = pivoted[~pivoted.participant.isin(outliersFriz)]
ax3 = sns.jointplot(noOutliersFriz['Frisbee_Rel_minus_Abs_Near'], noOutliersFriz['Frisbee_Rel_minus_Abs_Far'], kind="reg")

ax2 = sns.jointplot(pivoted['Nav_Rel_minus_Abs_Near'], pivoted['Nav_Rel_minus_Abs_Far'], kind="reg")

outliersNav = ['61216562','64824344','58839785']
noOutliersNav = pivoted[~pivoted.participant.isin(outliersNav)]
ax4 = sns.jointplot(noOutliersNav['Nav_Rel_minus_Abs_Near'], noOutliersNav['Nav_Rel_minus_Abs_Far'], kind="reg")


ax6 = sns.jointplot(pivoted['Nav_Rel_minus_Abs'], pivoted['Frisbee_Rel_minus_Abs'], kind="reg")
ax1.set_axis_labels('Navigation Relative Minus Absolute', 'Frisbee Relative Minus Absolute')
plt.xlim(-.6,.6)
plt.ylim(-.6,.6)

outliersBetween = ['52817250']
noOutliersBetween = pivoted[~pivoted.participant.isin(outliersBetween)]
ax5 = sns.jointplot(noOutliersBetween['Nav_Rel_minus_Abs'], noOutliersBetween['Frisbee_Rel_minus_Abs'], kind="reg")


# <codecell>
#Boxplots

plt.figure()
ax6 = sns.boxplot(data=merged,x='Friz_Force_Preference',y="Frisbee")
plt.figure()
ax7 = sns.boxplot(data=merged,x='Sex',y="Frisbee")
plt.figure()
ax8 = sns.boxplot(data=merged,x='Sex',y="Navigation")
plt.figure()
ax9 = sns.boxplot(data=merged,x='Friz_Force_Preference',y="Navigation")


# <codecell>
#Additional scatters
ax1 = sns.jointplot(pivotedAllFour['Navigation']['Left'], pivoted['Nav_Rel_minus_Abs'], kind="reg")
ax1 = sns.jointplot(pivotedAllFour['Navigation']['Right'], pivoted['Nav_Rel_minus_Abs'], kind="reg")
ax1 = sns.jointplot(pivotedAllFour['Navigation']['Home'], pivoted['Nav_Rel_minus_Abs'], kind="reg")

### <codecell>
ax1 = sns.jointplot(pivotedAllFour['Friz_Back_minus_Fore'], pivoted['Frisbee_Rel_minus_Abs'], kind="reg")


# <codecell>
#Statistical Tests


#Greater rel bias for nav than friz
ttestdata = pivoted['Nav_Rel_minus_Abs']-pivoted['Frisbee_Rel_minus_Abs']
t,prob = scipy.stats.ttest_1samp(ttestdata,0)

fb = merged[merged['Friz_Force_Preference'] == 'Forehand / Backhand']
ha = merged[merged['Friz_Force_Preference'] == 'Home / Away']
 
   
t = []
p = []
for i,j in enumerate(fb):
    if fb[j].dtype == 'float64':
        print(j, scipy.stats.ttest_ind(fb[j],ha[j]))
    
m = merged[merged['Sex'] == 'male']
f = merged[merged['Sex'] == 'female']

t2 = []
p2 = []
for i,j in enumerate(f):
    if f[j].dtype == 'float64':
        print(j, scipy.stats.ttest_ind(m[j],f[j]))

#T-Tests 2 
        
h = merged[merged['Friz_Position'].isin(['Handler','Both'])]
cb = merged[merged['Friz_Position'] == 'Cutter']  

for i,j in enumerate(h):
    if h[j].dtype == 'float64':
        print(j, scipy.stats.ttest_ind(h[j],cb[j]))
 
    


# <codecell>
#Plot influence graph of outliers
fig,ax = plt.subplots(figsize=(12,8))
lm = sm.OLS(pivoted['Nav_Rel_minus_Abs_Near'], pivoted['Nav_Rel_minus_Abs_Far']).fit()
fig = sm.graphics.influence_plot(lm,alpha=0.001,ax=ax,criterion="cooks")



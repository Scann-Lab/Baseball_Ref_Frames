dataForRT_for_R <- read.csv("C:/Users/smwei/Dropbox/Penn Post Doc/Frisbee_Ref_Frames/analysis/Ultimate/scripts/dataForRT_for_R.csv")

myData <- dataForRT_for_R

myData.mean <- aggregate(myData$Trials_responsert,
                         by = list(myData$participant, myData$stimLoc,
                                   myData$promptType, myData$condition),
                         FUN = 'mean')

colnames(myData.mean) <- c("participant","stimLoc","promptType","condition","Trials_responsert")

myData.mean <- myData.mean[order(myData.mean$participant), ]
head(myData.mean)

rt.aov <- with(myData.mean,
                   aov(Trials_responsert ~ stimLoc * promptType * condition +
                         Error(participant / (stimLoc*promptType*condition)))
)



library(ez)
library(lme4)

ezANOVA(data = dataForRT_for_R, dv=Trials_responsert, wid = participant, within=c(promptType,stimLoc,condition))
friz <- dataForRT_for_R[dataForRT_for_R$condition == "Frisbee",]
nav <- dataForRT_for_R[dataForRT_for_R$condition == "Navigation",]
ezANOVA(data = friz, dv=Trials_responsert, wid = participant, within=c(promptType,stimLoc))
ezANOVA(data = nav, dv=Trials_responsert, wid = participant, within=c(promptType,stimLoc))



        
unrestricted_fit <- lmer(Trials_responsert ~ stimLoc * condition * promptType + (1 | participant), data=dataForRT_for_R, REML=F)
#next, compute a model where the effect of status is not estimated
restricted_fit <- lmer(Trials_responsert ~ condition + (1 | participant), data=dataForRT_for_R, REML=F)
#compute the AIC-corrected log-base-2 likelihood ratio (a.k.a. "bits" of evidence)
(AIC(restricted_fit)-AIC(unrestricted_fit))*log2(exp(1))






ezANOVA(data = dataForRT_for_R, dv=Trials_responsert, wid = participant, within=c(promptType,stimLoc,condition),between = Sex)



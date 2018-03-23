myData <- data_for_R

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

ezANOVA(data = data_for_R, dv=Trials_responsert, wid = participant, within=c(prompt1,stimLoc,condition))
        
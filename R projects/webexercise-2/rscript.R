library(ggplot2)
alzheimers_data <- read.csv("Alzheimer_s_Disease.csv")
data_2017 <- alzheimers_data[alzheimers_data$Year == 2017,]

mean_outcome <- aggregate(data_2017[,
c("Total_MaleRate", "Total_FemaleRate", "TotalRate")],
by=list(Outcome = data_2017$OUTCOME), FUN=mean, na.rm=TRUE)
print(mean_outcome)


ggplot(data = mean_outcome, aes(x = mean_outcome$Outcome, y = mean_outcome$TotalRate)) + 
  geom_bar(stat="identity",aes(fill= factor(mean_outcome$Outcome)),
           width=0.5) +
  ggtitle("Total Rates of Alzheimers Outcomes in San Diego County")+
  ylab("Mean of Total Rates") +
  xlab("Outcomes") +
  theme(axis.text.x = element_text(angle=70, vjust=1, hjust=1))+
  list()


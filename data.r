library(statsr)
library(dplyr)
library(ggplot2)

loss <- read.csv("loss.csv", header=FALSE)
reward <- read.csv("reward.csv", header=FALSE)
colnames(loss) <- c("epoch", "loss")
colnames(reward) <- c("epoch", "reward")


ggplot(loss, aes(x=epoch, y=loss)) + ylim(0, 0.00001) + xlim(0, 500) + geom_point()
ggplot(reward, aes(x=epoch, y=reward)) + xlim(0, 90000) + geom_point()

eindhoven <- read.csv("eindhoven.csv")

#summary
summary(eindhoven)

#head
head(eindhoven)

#number of observations
nrow(eindhoven)

#apparently all variables is classed as character, fist thing to adjust when cleaning data in dPrep (In order to make summary statistics such as the average price or selling duration)
class(eindhoven$Aangeboden.sinds)
class(eindhoven$Laatste.vraagprijs)

#check which columns contain NA's
apply(eindhoven, 2, function(x) any(is.na(x)))

#interesting... a lot of columns contain NA's, pay attention to this in the cleaning proces

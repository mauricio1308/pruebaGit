# INGENIERÍA FINANCIERA
# Sergio Cabrales s-cabral@uniandes.edu.co
#################################################

#install.packages('quantmod')
library("quantmod")

# Apple
getSymbols("AAPL", from = "2020-01-01") 

getQuote("AAPL")

# daily,weekly,monthly,quarterly, and yearly 
dailyReturn(AAPL) # returns by day 
weeklyReturn(AAPL) # returns by week 
monthlyReturn(AAPL) # returns by month, indexed by yearmon 

allReturns(AAPL) # note the plural

#Charting
barChart(AAPL)

# Return and Volatility I
ret <-  dailyReturn(AAPL, type='log')
vol <- sd(ret, na.rm=TRUE)*sqrt(252)
vol

# Return and Volatility II
ret2 <-  log(AAPL$AAPL.Adjusted) - log(lag(AAPL$AAPL.Adjusted)) 
vol2 <- sd(ret2, na.rm=TRUE)*sqrt(252)
vol2

n <- length(AAPL$AAPL.Adjusted)
ret3 <- log(AAPL$AAPL.Adjusted[2:n])- log(lag(AAPL$AAPL.Adjusted[1:(n-1)]))
vol3 <- sd(ret3,na.rm=TRUE)*sqrt(252)

import pandas as pd

data_csv_name = "BuyingLosers.csv"
stop_loss = -0.5
ceiling = 0.005

df = pd.read_csv(data_csv_name)

sum_returns = 0
total_cash = 1000
loser_ceiling = 0
loser_stop = 0
loser_eod = 0
winner_stop = 0
winner_ceiling = 0
winner_eod = 0

for index, row in df.iterrows():
    percent_return = float(row['% Return'])
    high_percent = float(row['High %'])
    low_percent = float(row['Low %'])
    if percent_return < 0:
        if high_percent >= ceiling:
            returns = ceiling # we'll have sold by now
            #print "Loser Ceiling Sell " + str(returns)
            loser_ceiling = loser_ceiling + 1
        elif low_percent <= stop_loss or percent_return <= stop_loss:
            returns = stop_loss # we'll have sold by now
            #print "Loser Stop Loss Sell " + str(returns)
            loser_stop = loser_stop + 1
        else:
            returns = percent_return # exit by end of day no matter what
            #print "Loser EOD Sell " + str(returns)
            loser_eod = loser_eod + 1
    else:
        if low_percent <= stop_loss:
            returns = stop_loss # we'll have sold by now
            #print "Winner StopLoss Sell " + str(returns)
            winner_stop = winner_stop + 1
        elif high_percent >= ceiling or percent_return >= ceiling:
            returns = ceiling # we'll have sold by now
            #print "Winner Ceiling Sell " + str(returns)
            winner_ceiling = winner_ceiling + 1
        else:
            returns = percent_return # exit by end of day no matter what
            #print "Winner EOD Sell " + str(returns)
            winner_eod = winner_eod + 1
    sum_returns = sum_returns - returns
    total_cash = total_cash * (1 - returns)

print "Returns: " + str(sum_returns)
print "Cash: " + str(total_cash)
print "Loser Ceiling: " + str(loser_ceiling)
print "Loser Stop: " + str(loser_stop)
print "Loser EOD: " + str(loser_eod)
print "Winner Stop: " + str(winner_stop)
print "Winner Ceiling " + str(winner_ceiling)
print "Winner EOD: " + str(winner_eod)

#for i in df.iterrows():
#    print i[1]
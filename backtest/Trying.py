from pyalgotrade import strategy, bar
import pyalgotrade
from pyalgotrade.barfeed import ninjatraderfeed

hello = ninjatraderfeed.Feed(pyalgotrade.bar.Frequency.MINUTE).addBarsFromCSV('AAPL','test.csv')

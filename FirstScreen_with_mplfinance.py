import pandas as pd
import matplotlib.pyplot as plt
import datetime
import mplfinance as mpf
import matplotlib.dates as mdates
from Investar import Analyzer

mk = Analyzer.MarketDB()
df = mk.get_daily_price('NAVER', '2020-03-18')
df.index = pd.to_datetime(df.date, format="%Y-%m-%d")
df = df[['open','high','low','close','volume']]

ema60 = df.close.ewm(span=60).mean() # 종가의 12주(60일) 지수 이동평균
ema130 = df.close.ewm(span=130).mean() # 종가의 26주(130일) 지수 이동평균
macd = ema60 - ema130
signal = macd.ewm(span=45).mean() # 신호선(MACD의 9주 지수 이동평균)
macdhist = macd - signal # MACD 히스토그램

apds = [mpf.make_addplot(ema130, color='c'), mpf.make_addplot(macdhist, type='bar',panel=1, color='m'),
        mpf.make_addplot(macd,panel=1, color='b'), mpf.make_addplot(signal,panel=1, color='g')]



mc = mpf.make_marketcolors(up='r',down='b', inherit=True)
stl = mpf.make_mpf_style(marketcolors=mc)
mpf.plot(df, title='Triple Screen Trading - First Screen (NAVER)', type='candle', addplot = apds, figsize=(9,7), panel_ratios=(1,1), style=stl)







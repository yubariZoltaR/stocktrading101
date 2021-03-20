import matplotlib.pyplot as plt
from Investar import Analyzer

mk = Analyzer.MarketDB()
df = mk.get_daily_price('NAVER', '2020-03-18')

df['MA20'] = df['close'].rolling(window=20).mean() #20일 이평선
df['stddev'] = df['close'].rolling(window=20).std()
df['upper'] = df['MA20'] + (df['stddev'] * 2)
df['lower'] = df['MA20'] - (df['stddev'] * 2)
df['PB'] = (df['close'] - df['lower']) / (df['upper'] - df['lower']) #%B(주가가 볼린저밴드 어디에 위치하는지)값 생성

df['II'] = (2* df['close'] - df['high'] - df['low']) / (df['high'] - df['low']) * df['volume'] #일중강도 II
df['IIP21'] = df['II'].rolling(window=21).sum() / df['volume'].rolling(window=21).sum()*100    #일중강도율 II%
df = df.dropna() #앞에서의 df[19:]와 같은 맥락으로 NA값 날리기


plt.figure(figsize=(13,10))
plt.subplot(3,1,1)
plt.plot(df.index, df['close'], 'b', label='Close')
plt.plot(df.index, df['upper'], 'r--', label = 'Upper band')
plt.plot(df.index, df['MA20'], 'k--', label = 'Moving average 20')
plt.plot(df.index, df['lower'], 'c--', label = 'Lower band')
plt.fill_between(df.index, df['upper'], df['lower'], color='0.9')
for i in range(0, len(df.close)):
    if df.PB.values[i] < 0.05 and df.IIP21.values[i] >0:
        plt.plot(df.index.values[i], df.close.values[i], 'r^')
    elif df.PB.values[i] > 0.95 and df.IIP21.values[i] <0:
        plt.plot(df.index.values[i], df.close.values[i], 'bv')


plt.legend(loc='best')
plt.title('NAVER Bollinger Band (20 day, 2 std) - Reversals')


plt.subplot(3,1,2)
plt.plot(df.index, df['PB'], color='b', label='%B')
plt.grid(True)
plt.legend(loc='best')


plt.subplot(3,1,3)
plt.bar(df.index, df['IIP21'], color='g', label='II% 21day')
for i in range(0, len(df.close)):
    if df.PB.values[i] < 0.05 and df.IIP21.values[i] >0:
        plt.plot(df.index.values[i], 0, 'r^')
    elif df.PB.values[i] > 0.95 and df.IIP21.values[i] <0:
        plt.plot(df.index.values[i], 0, 'bv')
plt.grid(True)
plt.legend(loc='best')
plt.show()



import matplotlib.pyplot as plt
from Investar import Analyzer

mk = Analyzer.MarketDB()
df = mk.get_daily_price('NAVER', '2020-03-18')

df['MA20'] = df['close'].rolling(window=20).mean() #20일 이평선
df['stddev'] = df['close'].rolling(window=20).std()
df['upper'] = df['MA20'] + (df['stddev'] * 2)
df['lower'] = df['MA20'] - (df['stddev'] * 2)
df['PB'] = (df['close'] - df['lower']) / (df['upper'] - df['lower']) #%B(주가가 볼린저밴드 어디에 위치하는지)값 생성
df['bandwidth'] = (df['upper'] - df['lower']) / df['MA20'] * 100 #밴드폭(상단밴드와 하단밴드 사이의 폭)
df['TP'] = (df['high'] + df['low'] + df['close']) / 3 #중심가격(TP) 구하기
df['PMF'] = 0
df['NMF'] = 0
for i in range(len(df.close)-1):
    if df.TP.values[i] < df.TP.values[i+1]:
        df.PMF.values[i+1] = df.TP.values[i+1] * df.volume.values[i+1]
        df.NMF.values[i+1] = 0
    else:
        df.NMF.values[i+1] = df.TP.values[i+1] * df.volume.values[i+1]
        df.PMF.values[i+1] = 0
df['MFR'] = df.PMF.rolling(window=10).sum() / \
            df.NMF.rolling(window=10).sum()             #10일동안의 PMF의 합을 NMF의 합으로 나눈 결과를 현금흐름비율(MFR)에 저장
df['MFI10'] = 100 - 100 / (1 + df['MFR'])       # MFI(현금흐름지표) 계산식
df = df[19:]

plt.figure(figsize=(13,10))
plt.subplot(3,1,1)
plt.plot(df.index, df['close'], color='#0000ff', label='Close')
plt.plot(df.index, df['upper'], 'r--', label = 'Upper band')
plt.plot(df.index, df['MA20'], 'k--', label = 'Moving average 20')
plt.plot(df.index, df['lower'], 'c--', label = 'Lower band')
plt.fill_between(df.index, df['upper'], df['lower'], color='0.9')
for i in range(len(df.close)):
    if df.PB.values[i] > 0.8 and df.MFI10.values[i] > 80:
        plt.plot(df.index.values[i], df.close.values[i],'r^')
    elif df.PB.values[i] < 0.2 and df.MFI10.values[i] < 20:
        plt.plot(df.index.values[i], df.close.values[i], 'bv')
plt.legend(loc='best')
plt.title('NAVER Bollinger Band (20 day, 2 std)')


plt.subplot(3,1,2)
plt.plot(df.index, df['PB'] * 100, color='b', label='%B x 100')
plt.plot(df.index, df['MFI10'], 'g--', label='MFI(10 day)')
plt.yticks([-20,0,20,40,60,80,100,120])
for i in range(len(df.close)):
    if df.PB.values[i] > 0.8 and df.MFI10.values[i] > 80:
        plt.plot(df.index.values[i], 0,'r^')
    elif df.PB.values[i] < 0.2 and df.MFI10.values[i] < 20:
        plt.plot(df.index.values[i], 0, 'bv')
plt.grid(True)
plt.legend(loc='best')


plt.subplot(3,1,3)
plt.plot(df.index, df['bandwidth'], color='m', label='bandwidth')
plt.grid(True)
plt.legend(loc='best')
plt.show()



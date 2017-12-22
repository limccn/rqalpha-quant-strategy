#HMM上证指数择时，这里做了两个HMM模型
import numpy as np
import pandas as pd

#000001.txt包含上证指数的所有日数据，需要自己把数据下载到本地
data=pd.read_table("D:/000001.txt",header=1).iloc[:-1,[0,1,2,3,4,5]]
data.columns=['date','open','high','low','close','volume']
data['V/MA']=data['volume']/data['volume'].rolling(15).mean() #成交量与过去15天平均成交量的比值
data=data.set_index('date')

data.index=pd.to_datetime(data.index)
data=data['2005':'2014'] #截取数据

#提取特征，做适当地缩放后，做fisher变换
O1=0.4*((data['close']-data['open'])/(data['high']-data['low'])).values
O1.shape=(len(O1),1)
O1=np.log((1+O1)/(1-O1))

O2=data['V/MA'].values/(data['high']/data['low']).values
O2.shape=(len(O2),1)
O2=0.2*np.log(O2)
O2=np.log((1+O2)/(1-O2))

#Ob1=np.hstack((O1,O2))
Ob1=O1 #第一个HMM模型的观测数据
Ob2=O2 #第二个HMM模型的观测数据

Return=(data['close']/data['open']-1).values #求出每一天的日对数收益率
from hmmlearn import hmm
len1=len(data[:'2010']) #2010年以前的数据作为训练数据
len2=len(data['2011':]) #2011年以后的数据作为回测数据
Signal=np.zeros(len2)
np.random.seed(1)
N_state1=3 #第一个HMM隐藏状态的个数设置为3
N_state2=4 #第二个HMM隐藏状态的个数设置为4

for i in range(len2):
    #滚动训练，每个月更新一次
    if data.index[len1+i-1].month!=data.index[len1+i].month: 
        remodel1=hmm.GaussianHMM(n_components=N_state1)
        remodel1.fit(Ob1[:len1+i])
        remodel2=hmm.GaussianHMM(n_components=N_state2)
        remodel2.fit(Ob2[:len1+i])
    s_pre1=remodel1.predict(Ob1[:len1+i]) #对历史数据做状态序列的预测
    s_pre2=remodel2.predict(Ob2[:len1+i])
    Re=Return[:len1+i] #取出历史数据的收益率序列
    #各个状态在历史数据中的平均收益率
    Expect=np.array([np.mean(Re[(s_pre1==j)*(s_pre2==k)]) \
                     for j in range(N_state1) for k in range(N_state2)])
    #各个状态在第二天的发生概率
    Pro=np.array([remodel1.transmat_[s_pre1[-1],j]*remodel2.transmat_[s_pre2[-1],k]\
                  for j in range(N_state1) for k in range(N_state2)])
    preReturn=Pro.dot(Expect) #根据转移概率矩阵预测下一天的期望收益
    if preReturn>0.:
        Signal[i]=1
sReturn=(data['close']/data['close'].shift(1))[len1:]-1 #回测阶段的日简单收益率
#考虑万分之六的交易成本
Cost=pd.Series(np.zeros(len(Signal)),index=sReturn.index) 
for i in range(1,len(Signal)):
    if Signal[i-1]!=Signal[i]:
        Cost.values[i]=0.0006
SignalRe=np.cumprod(Signal*(sReturn-Cost)+1)-1 #策略的累计收益率
IndexRe=np.cumprod(sReturn+1)-1 #基准的累计收益率
import matplotlib.pyplot as plt
plt.figure(figsize=(10,5))
plt.plot(IndexRe,label='Index')
plt.plot(SignalRe,label='Signal')
plt.plot(SignalRe-IndexRe,label='excess')
plt.axhline(y=1)
plt.axhline(y=0.5)
plt.legend()
plt.show()
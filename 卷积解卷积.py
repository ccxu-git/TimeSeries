# %matplotlib auto
# %matplotlib inline
##
import numpy as np
from serana import myFFT
import figure as fig
pi = np.pi

# 时间段，按天采样
dt = 1/365.24/4  # 采样间隔
time = np.arange(1800, 2019, dt).reshape(-1, 1)       # (L1,1)
N = time.shape[0]  # 数据长度

# 生成模拟的激发序列
Per = np.array([[1, 2, 3, 4, 5, 7, 8, 13.5, 18.6]])   # (1,L2)
Amp = np.array([1, 1, 0.5, 0.5, 0.2, 0.2, 1, 1, 1 ])*0      # 普通的一维数组
ser_ext0 = np.cos(2*pi/Per*time).dot(Amp)
    # 数组的运算规则(L1,1)*(1,L2)=(1,L2)*(L1,1)=>(L1,L2)
    # np.max(Per*time - time*Per) >> 0
ser_ext = ser_ext0 + np.random.randn(N)*0.5                # 加随机噪声
fig.plot(time, ser_ext)                                    # 绘制激发函数的时间序列
fig.set(xlim=(1800, 2019), xlabel='Time (year)', show=1,
        ylabel='Amplitude', title='激发函数')

## 计算卷积后的序列
Q = 51.6                     # Q value of Duan 2017.
P = 5.9                      # Period of SYO
B = 2*pi/P/Q                 # y'' + B*y' + C*y = f
C = ((4*pi/P)**2 + B**2)/4   # B和C是上述二阶常系数非齐次线性微分方程的系数
# 参数初始化完成，下面计算卷积序列
y = np.zeros(shape=(N, 1))           # y[0]=y'[0]=0
for i in range(1, N-1):
    tmp = dt**2*ser_ext[i] - (C*dt**2 - 2)*y[i] - (1 - B*dt/2)*y[i-1]
    y[i+1] = tmp / ( B*dt/2 + 1 )
fig.plot(time, y)
fig.set(xlim=(1800, 2019), xlabel='Time (year)',
         ylabel='Amplitude', title='卷积的时间序列')

# 卷积序列与激发序列的频谱图对比
myFFT(y, dt=dt, x_type='Per', result='f1')
myFFT(ser_ext, dt=dt, x_type='Per', result='f1', holdon=True)
fig.set(xlim=(0, 20), xlabel='Periods (year)',
        ylabel='Amplitude', title='频谱图',
        labels=['卷积序列', '激发函数'])

## 解卷积
ser_ext_ds = ser_ext[::4]
time_ds = time[::4]
y_ds = y[::4]
N_ds = len(y_ds)
# 先降采样
fd = np.zeros(shape=(N_ds, 1))    # y[0]=y'[0]=0
fd[0], fd[-1] = ser_ext[0], ser_ext[-1]
for i in range(1, N_ds-1):
    fd[i] = ( ( B*(dt*4)/2 + 1 )*y_ds[i+1] +
              ( 1 - B*(dt*4)/2 )*y_ds[i-1] +
              (C*(dt*4)**2 - 2)*y_ds[i]  ) / (dt*4)**2

# 时域对比
fig.plot(time, ser_ext, label='模拟的激发函数(dt=6h)')
fig.plot(time_ds, fd, label='解卷积序列(dt=1d)', holdon=True)
fig.set(xlim=(1800, 2019), xlabel='Time (year)',  ylabel='Amplitude')

# 频域对比
myFFT(ser_ext, dt=dt, x_type='Frq', result='f1')
myFFT(fd, dt=dt*4, x_type='Frq', result='f1', holdon=True)
fig.set(xlim=(0, 150), ylim=(0, 0.007),
        xlabel='Frequency (cpy)', ylabel='Amplitude', title='频谱图',
        labels=['模拟的激发函数(dt=6h)', '解卷积序列(dt=1d)'])

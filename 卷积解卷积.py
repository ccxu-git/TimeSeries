##
import numpy as np
from serana import myFFT
pi = np.pi

# 时间段，按天采样
dt = 1/3  # 采样间隔
time = np.arange(1800, 2019, dt).reshape(-1, 1)       # (L1,1)
N = time.shape[0]  # 数据长度

# 生成模拟的激发序列
Per = np.array([[1, 2, 3, 4, 5, 6, 7, 8, 13.5, 22]])  # (1,L2)
Amp = np.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1 ])       # 普通的一维数组
ser_ext0 = np.cos(2*pi/Per*time).dot(Amp)
    # 数组的运算规则(L1,1)*(1,L2)=(1,L2)*(L1,1)=>(L1,L2)
    # np.max(Per*time - time*Per) >> 0
ser_ext = ser_ext0 + np.random.randn(N)               # 加随机噪声
# plt.plot(time, ser_ext)  # 绘图
# 绘制激发序列的频谱图
myFFT(ser_ext, dt=dt, x_type='Frq', flag_return='f2')

# 计算卷积后的序列

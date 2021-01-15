# -*- encoding: utf-8 -*-
'''
    @File Name   : figure.py
    @Description : 绘图工具
    @Create Time : 2021/01/12 12:52:09
    @The Author  : Can-Can Hsu
'''
##
from matplotlib import pyplot as plt
import matplotlib.style as mplstyle
import os

# 设置快速样式,加快绘图速度.并确保fast在最后
# https://blog.csdn.net/jeffery0207/article/details/81317000
mplstyle.use(['seaborn-deep', 'fast'])
# matplotlib绘图风格,参考下面链接. seaborn-deep效果不错
# https://blog.csdn.net/justisme/article/details/100543869

# 解决标签无法显示中文的问题, 参考链接如下
# https://blog.csdn.net/weixin_43343803/article/details/90551321
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

container = []  # 容器, 用于放置axes

## 绘图工具
def plot(x, y, linewidth=0.75, label=None, holdon=False):
    
    # 默认新建图窗
    if not holdon: new()

    # 绘图
    if label is None or label == '':
        ax = plt.plot(x, y, linewidth=linewidth)
    else:
        ax = plt.plot(x, y, linewidth=linewidth, label=label)
        plt.legend(loc='best', frameon=False, ncol=2)
    container.extend(ax)
    # 绘制格网
    plt.grid(b=True, linestyle='-.', linewidth=0.5)

def set(xlim=None, ylim=None,
        title=None, titlesize=12, labels=None,
        xlabel=None, ylabel=None, labelsize=12,
        show=False):
    # limit
    if   xlim is not None: plt.xlim(xlim[0], xlim[1])
    if   ylim is not None: plt.ylim(ylim[0], ylim[1])
    # title
    if  title is not None: plt.title(title,  fontsize=titlesize)
    # legend
    if labels is not None: legend(labels=labels, show=show)
    # x/y label
    if xlabel is not None: plt.xlabel(xlabel, fontsize=labelsize)
    if ylabel is not None: plt.ylabel(ylabel, fontsize=labelsize)
    # show
    if show: showing()

# 仅设置axes.lines里的legend
def legend_lines(labels=None, show=False):
    lines_gca = plt.gca().lines
    for i, l in enumerate(lines_gca):
        if labels[i] == '': continue
        l.set_label(labels[i])
    plt.legend(loc='best', frameon=False, ncol=2)
    # show
    if show: showing()

# 设置container里每一个axes的Legend
def legend(labels=None, show=False):
    # 如果lables是str类型,将其转为list
    if isinstance(labels, str): labels = [labels]
    # 逐一设置label
    for i, c in enumerate(container):
        if labels[i] == '': continue
        c.set_label(labels[i])
    plt.legend(loc='best', frameon=False, ncol=2)
    # show
    if show: showing()

def new():  # 清空容器, 创建新fig
    container.clear()
    plt.figure()

def save(filename='tmp.svg', path=None):
    # 获取存储路径
    if path is None: path = os.getcwd() + '/'
    # 判断路径的末尾是否存在'/'或'\\',若不存在则添加'/'
    if path[-1] != '/' and path[-2:] != '\\':
        path = path + '/'
    plt.savefig( path + filename )

def showing():  # 清空容器, 展示fig
    container.clear()
    # if backen is not None:
    #     plt.switch_backend(backen)
    # else:
    #     backen = 'TkAgg'
    # # 判断启用的是否是webagg
    # if backen.lower() == 'webagg':
    #     import nest_asyncio
    #     nest_asyncio.apply()
    # show完不需关闭，程序自动向下执行
    plt.ion()
    # show完不需关闭，程序自动向下执行
    plt.show()

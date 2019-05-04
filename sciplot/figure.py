# -*- coding: utf-8 -*-

import matplotlib
import matplotlib.pyplot as plt
import os
import numpy as np
# plt.subplots_adjust(top = 1, bottom = 0, right = 1, left = 0, hspace = 0, wspace = 0)


def cm2inch(value):
    return value/2.54


# 将ps转为pdf，利用gmt的程序可以切边
def ps2pdf(filename_fig, dpi=720):
    os.system('gmt psconvert '+filename_fig+'.ps -Tf -Au -V -E'+str(dpi))
    # os.system('rm '+filename_fig+'.ps')

# transform pdf or eps to svg


def pdf2svg(filename_fig):
    os.system('pdf2svg '+filename_fig+'.pdf '+filename_fig+'.svg')

# 将ps转为png，利用gmt的程序可以切边


def ps2png(filename_fig, dpi=300):
    os.system('gmt psconvert '+filename_fig+'.ps -Tg -Au -V -E'+str(dpi))
    # os.system('rm '+filename_fig+'.ps')


# 根据几个给定的模式返回figure size
def figsize(model='full', ratio='16:9', x=[], y=[], ratio_adjust_height=1, scale=1):
    # model: full, half, quater
    # ratio: 16:9, 4:3, xy (根据x和y数据的比例进行调整，必须给出x和y)
    # ratio_adjust_height: 对于按照数据比例计算的纵横高度，由于label的原因高度会被低估，根据第一次绘图结果估计一个
    # 系数，ratio_adjust_height乘以计算之后的高度，一般会大于1
    # scale: 在计算所得的尺寸基础上乘以scale
    figsize_style = np.array(
        matplotlib.rcParams['figure.figsize'], dtype=float)
    figwidth = (figsize_style[0])
    # figheight = (figsize_style[1])
    # figure width 固定，根据ratio调整figure height
    if(ratio == '16:9'):
        factor = 9/16
    elif(ratio == '4:3'):
        factor = 3/4
    elif(ratio == 'xy'):
        factor = 1
        if(((len(x) == 0) | (len(y) == 0))):
            print('如果ratio为xy，则必须给出x向量和y向量来计算数据纵横比\n计算失败，默认纵横比例为16:9')
            factor = 9/16
        else:
            length_x = np.max(x)-np.min(x)
            length_y = np.max(y)-np.min(y)
            factor = length_y/length_x*ratio_adjust_height
    elif(len(ratio.split(':')) == 2):
        ratio = np.array(ratio.split(':'), dtype=float)
        factor = ratio[1]/ratio[0]
    else:
        factor = 9/16
    if(model == 'full'):
        return [figwidth*scale, figwidth*factor*scale]
    elif(model == 'half'):
        return [figwidth/2*scale, figwidth*factor/2*scale]
    else:
        return [figwidth*model*scale, figwidth*factor*model*scale]


# 获取一个颜色序列：比如线条颜色循环
def colors(index=1, model='auto'):
    if(model == 'auto'):
        colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
                  '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
        return colors[index % len(colors)]
    else:
        colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
                  '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
        return colors[index % len(colors)]


# 配置图片的主体字体和数学字体，以及其他选项，后面再填
def conf(fontname="Times New Roman", mathfont='cm'):
    # -------------------------------------------------------------------------------
    # 配置字典设置
    #	print path.abspath(matplotlib.matplotlib_fname())	#当前使用的配置文件
    # matplotlib.rcParams["figure.autolayout"] = "TRUE"  # 图片边距
    matplotlib.rcParams["font.family"] = fontname
    # 公式字体:tt, it, rm, cal, sf, bf or default/regular (non-math)
    # matplotlib.rcParams["mathtext.default"] = "regular"  #公式字体与正文字体一致: it, regular
    # 公式字体与latex公式字体一致：cm, stix, stixsans
    matplotlib.rcParams["mathtext.fontset"] = mathfont
    # matplotlib.rcParams['ps.fonttype'] = 42  # 保存的pdf文字可以在AI 中编辑
    matplotlib.rcParams['pdf.fonttype'] = 42


# 获取默认线宽的倍数，以便自动化：paper和keynote两种模式
def linewidth(factor=1):
    linewidth = matplotlib.rcParams['lines.linewidth']
    return linewidth*factor


def help():
    print('fig=plt.figure(figsize=scifig.figsize("full",ratio="1:2"))')
    print('# .... ')
    print(r'# save fig')
    print(r'plt.tight_layout(pad=0,h_pad=0,w_pad=0)')
    print(r'figpath="../analysis/nature/2018-2018"')
    print(r'filename_fig=figpath+"/bar_num_papers_subjects"')
    print(r'plt.savefig(filename_fig+".pdf")')
    print(r'plt.savefig(filename_fig+".png",dpi=1200)')

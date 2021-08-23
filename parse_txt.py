# -*- coding: utf-8 -*-
"""
Created on Tue Jul  9 13:27:43 2019

@author: Administrator
"""

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#fp = open('test.txt', "r")
# 變數 lines 會儲存 filename.txt 的內容
#lines = fp.readlines()
# close file
#fp.close()
#lines = lines[26:]
#df = pd.DataFrame(lines)
#
#
#df = pd.DataFrame(df[0].str.split(expand = True))
#col = df.iloc[0]
#unit = df.iloc[1]

#BG_in = pd.read_csv('BG.txt',sep = '\t', encoding='big5')
#By_in = pd.read_csv('By.txt',sep = '\t', encoding='big5')

##clear space

#unit = df.iloc[0]
def format_data(df):
    col = df.columns
    unit = df.iloc[0]
    colname = []
    for n,i in enumerate(col):
        colname.append(i.replace(' ','') + unit[n].replace(' ',''))
    
    df = df.iloc[1:]
    df.columns = colname
    df = df.astype(float)
    
    return df

#BG = format_data(BG_in)
#By = format_data(By_in)
#
#ax = np.array(BG[BG.columns[0]])
#ay = np.array(BG[BG.columns[1]])
#By_y = np.array(By[By.columns[1]])
#diff = By_y - BG_y
#
#plt.plot(x,BG_y,'.',x,By_y,'.',x,diff)

#建立input data類別
class input_data:
    
    def __init__(self): 
          self._x = 0
          self._y = 0
    
    def get_xval(self):
        return self._x
    
    def get_yval(self):
        return self._y
    
    def set_xval(self,m):
        self._x = m
    
    def set_yval(self,m):
        self._y = m


def test(input_data,b):
    input_data.set_xval(b)
#a = 0
#def set_val(b):
#    global a 
#    a = b



#fitting
#讀取.dat資料
filename = 'd12_SW_A10-IntegratedB.txt'

def get_data(filename):
    #輸入檔名並解析成dataframe format, 副檔名須為.dat
    with open(filename) as f:
        
        lines = f.readlines()
        
        df = pd.DataFrame(lines)
        df = pd.DataFrame(df[0].str.split(expand = True))
        col = df.iloc[0]
        unit = df.iloc[1]
        colname = []
        for n,i in enumerate(col):
            colname.append(i.replace(' ','') + unit[n].replace(' ',''))
            
        df.columns = colname
        df = df.iloc[2:]
        df = df.astype(float)
    #    print(df)
        f.close()
        
    return df

get_data(filename)
#回傳fitting係數
def polyfit_coeff(x,y,order):
#    #檢查輸入資料格式
#    if type(df) != pd.core.frame.DataFrame and type(df) != list:
#        return 'Please check the format of input arguments!'
#
#    else:   
#        #polyfit
    coeff = np.polyfit(x,y,order)
    return coeff

#回傳fitting後的data
def fitting_data(x,coeff):
    
    fc = np.poly1d(coeff)
    fy = fc(x)  #fitting y
    
    return fy

#example
#df = get_data('C:/Users/Administrator/Documents/MEGA/Python/NSRRC/B field analysis/d12_SW_A10-IntegratedB.txt')
#coeff = polyfit_coeff(df,'Ix(G-cm)',2)
#fitting_data = fitting_data(df,coeff)     

x1 = np.arange(-25,18,0.05)
y1 = np.sin(x1)

#with open('dense.txt','w') as f:
#    f.write('x\t')
#    f.write('y\n')
#    f.write('(cm)\t')
#    f.write('(gauss)\n')
#    
#    for i in range(len(x1)):
#        f.write("%.2f" % x1[i] + '\t')
##        f.write('\t')
#        f.write("%.3f" % y1[i] + '\n')
##        f.write('\n')
##        print(x1[i],y1[i])
#    f.close()




#df = pd.read_csv('dense.txt',sep = '\t')
#df = df.iloc[1:]
#df = df.astype(float)


def count_digits(x):
    s = str(x).split('.')
    
    if len(s) == 1:
        return [x,0]
    
    elif len(s) == 2:
        digits = len(s[1])
        return [x,digits]

def float_sub_format(a,b):
    
    n = 10 ** int(max([a[1],b[1]]))
    k = 10 ** -int(max([a[1],b[1]]))
    res = int(b[0] * n  - a[0] * n) * k
    
    return res
    
    
#a = count_digits(0.79)
#b = count_digits(0.2)
#        
#res = float_sub_format(a,b)
#
#
##print((x1[-1]-x1[0])/ len(x1))
#
#x2 = np.arange(-25,18,0.5)
#y2 = np.sin(x2)
#
#with open('sparse.txt','w') as f:
#    f.write('x\t')
#    f.write('y\n')
#    f.write('(cm)\t')
#    f.write('(gauss)\n')
#    
#    for i in range(len(x2)):
#        f.write("%.2f" % x2[i] + '\t')
##        f.write('\t')
#        f.write("%.3f" % y2[i] + '\n')
##        f.write('\n')
##        print(x1[i],y1[i])
#    f.close()
#
#
#
#plt.plot(x1,y1,'.-',x2,y2,'r.-')
# =============================================================================
# 
# =============================================================================
df = pd.read_csv('sparse.txt',sep = '\t')
df = df.iloc[1:]
df = df.astype(float)

x = np.array(df[df.columns[0]])
y = np.array(df[df.columns[1]])
dx = 0.5
start = x[0]
dxx = 5
segs = [x[0],x[0]+dxx,x[0]+ 2*dxx,x[0]+3*dxx,]


def find_2adjacent(array, value,type,pos):
           
    if np.where(array == max(array))[0][0] == len(array) - 1 and value >= array[-1]:
        return array[-1]
    
    elif np.where(array == min(array))[0][0] == 0 and value <= array[0]:
        return array[0]
    
    elif len(np.where(array == value)[0]) != 0:
        if pos == 'later':
            return array[np.where(array == value)[0][0] - 1]
        elif pos == 'former':
            return array[np.where(array == value)[0][0]]
    
    else:
        array = np.asarray(array)
        diff = np.abs(array - value)
        idx1 = diff.argmin()
        diff[idx1] = np.abs(array).mean()
        idx2 = diff.argmin()
        index = [idx1,idx2]
        index.sort()

        if type == 'Upper':
            return array[index[1]]
        
        elif type == 'Lower':
            return array[index[0]]

def Riemann_sum(dx,x,y,segs):
    #integral
#    I = dx * y
    x_segs = []
#    I_segs = []
    for i in range(len(segs) - 1):
        index1 = np.where(x == find_2adjacent(x, segs[i],'Upper','former'))[0][0]
        index2 = np.where(x == find_2adjacent(x, segs[i+1],'Lower','later'))[0][0]
        x_seg = x[index1:index2 + 1]
        x_segs.append(x_seg)
#        I_seg = I[index1:index2 + 1]
#        I_segs.append(I_seg)
#        print(I_seg)
    
    return x_segs


Ixsegs = Riemann_sum(dx,x,y,segs)



def opendf(name):
    df = pd.read_csv(name,sep = '\t')
    df = format_data(df)
#                print(np.array(df[df.columns[0]]))
#                print(np.array(df[df.columns[1]]))
#                print(df)
    return [np.array(df[df.columns[0]]),np.array(df[df.columns[1]])]

#df = pd.read_csv('d14_Hall_BG_Bx-Orbit.txt')
#
#BGx1 = opendf('C:/Users/Administrator/Desktop/compa/621/d14_Hall_BG/Bx/d14_Hall_BG_Bx-Orbit.txt')
#BGy1 = opendf('C:/Users/Administrator/Desktop/compa/621/d14_Hall_BG/By/d14_Hall_BG_By-Orbit.txt')
#BGx2 = opendf('C:/Users/Administrator/Desktop/compa/801/d02_Hall_BG/Bx/d02_Hall_BG_Bx-Orbit.txt')
#BGy2 =opendf('C:/Users/Administrator/Desktop/compa/801/d02_Hall_BG/By/d02_Hall_BG_By-Orbit.txt')
#X1 = opendf('C:/Users/Administrator/Desktop/compa/621/d17_Hall_D2/Bx/d17_Hall_D2_Bx-Orbit.txt')
#Y1 = opendf('C:/Users/Administrator/Desktop/compa/621/d17_Hall_D2/By/d17_Hall_D2_By-Orbit.txt')
#X2 = opendf('C:/Users/Administrator/Desktop/compa/801/d13_Hall_D2/Bx/d13_Hall_D2_Bx-Orbit.txt')
#Y2 = opendf('C:/Users/Administrator/Desktop/compa/801/d13_Hall_D2/By/d13_Hall_D2_By-Orbit.txt')
#


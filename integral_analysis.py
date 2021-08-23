#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 16 17:45:49 2019

@author: victor
"""

# coding=utf-8
#import decimal

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
#import matplotlib
#matplotlib.use("TkAgg")
import math
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename

import numpy as np
import pandas as pd

 #define data class
class input_data():

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


class IntegralAnalysis(tk.Tk):

    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)

#        tk.Tk.iconbitmap(self, default="clienticon.ico")
        tk.Tk.wm_title(self, "Integral analysis for hall probe measurment")
        
        
        container = tk.Frame(self,bg = "white")
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        F = Graph
        
#        for F in (StartPage, PageOne, PageTwo, PageThree):

        frame = F(container, self)

        self.frames[F] = frame

        frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(F)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()


class Graph(tk.Frame):
    
    def __init__(self, parent, controller):
        
        #創一個大frame準備放入widgets
        def set_value_remind():
            showinfo("Warning", "Please set value for segments!")
        
        def nondivisible_warn():
            showinfo("Warning", "Please set a value which makes it divisible.")
        
        def data_format_warn():
            showinfo("Warning", "Please make sure the format of data is correct.")
        
        def negative_value_warn():
            showinfo("Warning", "Segment value must be positive.")
            
        def overrange_warn():
            showinfo("Warning", "Start point is out of range!")    
        
        #向上取值
        def find_2adjacent(array, value,type,pos):
            try:
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
                    
                    if type == 'Lower':
                        return array[index[0]]
                    
            except:
                pass
            
   
        def find_nearest(array, value):
            array = np.asarray(array)
            idx = (np.abs(array - value)).argmin()
            return array[idx]
        
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
        
         #Bx data segments calculation 
        def Bxseg_init():
            #Bx場
            #integral unit
            BxSegUnit = entryBxSegments.get()
    #            print(entryText)
            #Remind
            if BxSegUnit == '':
                set_value_remind()
            
            elif float(BxSegUnit) < 0:
                negative_value_warn()
                
            else:
                Bx_x = self.Bx_x
                Bx_y = self.Bx_y
                BxStart_2plot = entryBxin.get()
        
                #dx
#                dx_Bx = decimal.Decimal(Bx_x[-1]-Bx_x[0])/decimal.Decimal(len(Bx_x)-1)
#                dx_Bx = decimal.Decimal(Bx_x[1]-Bx_x[0])
                #算dx會有float precision的問題
                num1 = count_digits(Bx_x[0])
                num2 = count_digits(Bx_x[1])
                dx_Bx = float_sub_format(num1,num2)
#                print(dx_Bx)            
                
                if BxStart_2plot == '':
#                    print('no input')
                    BxStart_2plot = float(Bx_x[0])   
                
                elif float(BxStart_2plot) < Bx_x[0] or float(BxStart_2plot) > Bx_x[-1]:
                    overrange_warn()
                    
                else:
                    BxStart_2plot = float(BxStart_2plot)
                    
                BxStart_2cal = find_2adjacent(Bx_x,BxStart_2plot,'Upper','former')
                
#                print(BxStart_2cal)    
                #Label the segs
#                    Bx_x = np.arange(0,50,0.1)
#                    Bx_y = np.sin(Bx_x)
#                    dx_Bx = 0.1
#                    BxSegUnit = 3
#                    BxStart = 0
                    
                    #slice
                BxStart_index = np.where(Bx_x == BxStart_2cal)[0][0]                   
                BxEnd = Bx_x[-1]
                BxSegNum = int(divmod(BxEnd-float(BxStart_2plot), float(BxSegUnit))[0])
#                    BxSegNum = int(math.ceil((BxEnd-float(BxStart))/float(BxSegUnit)))
                Bxsegs = [float(BxStart_2plot)] + [float(BxSegUnit) * (i+1) + float(BxStart_2plot) for i in range(BxSegNum)] 
#                    Bxsegs_2cal = [float(BxStart_2cal)] + [float(BxSegUnit) * (i+1) + float(BxStart_2cal) for i in range(BxSegNum)] 

                ymean_Bx = (np.max(Bx_y) + np.min(Bx_y))/2
                Bx_NperSet = math.ceil(float(BxSegUnit) / dx_Bx)
                
#                print(BxStart_2plot,BxSegNum,Bxsegs)
    
                return [dx_Bx,BxStart_2plot,BxEnd,BxStart_index,BxSegNum,Bxsegs,ymean_Bx,Bx_NperSet]
        
        #By data segments calculation            
        def Byseg_init():
 
            #integral unit
            BySegUnit = entryBySegments.get()
    #            print(entryText)
            #Remind
            if BySegUnit == '':
                set_value_remind()
                
            elif float(BySegUnit) < 0:
                negative_value_warn()    
                
            else:
                By_x = self.By_x
                By_y = self.By_y
                ByStart_2plot = entryByin.get()
                
                #dx
#                dx_By = decimal.Decimal(By_x[1]-By_x[0])
                num1 = count_digits(By_x[0])
                num2 = count_digits(By_x[1])
                dx_By = float_sub_format(num1,num2)              
#                dx_By = (By_x[1]-By_x[0])

                if ByStart_2plot == '':
                    ByStart_2plot = By_x[0]
                
                elif float(ByStart_2plot) < By_x[0] or float(ByStart_2plot) > By_x[-1]:
                    overrange_warn()
                
                else:
                    ByStart_2plot = float(ByStart_2plot)
                
                ByStart_2cal = find_2adjacent(By_x,ByStart_2plot,'Upper','former')
                    
                #Label the segs
                #nondivisible remind
#                if float(BySegUnit) == 0 or decimal.Decimal(BySegUnit) % decimal.Decimal(str(dx_By)) != 0:
#                    nondivisible_warn()
                
#                else:
                    #slice         
                ByStart_index = np.where(By_x == ByStart_2cal)[0][0]
                ByEnd = By_x[-1]
                BySegNum = int(divmod(ByEnd-float(ByStart_2plot) , float(BySegUnit))[0])
    #                    BySegNum = int(math.ceil((ByEnd-float(ByStart))/float(BySegUnit)))
                Bysegs = [float(ByStart_2plot)] + [float(BySegUnit) * (i+1) + float(ByStart_2plot) for i in range(BySegNum)]
                ymean_By = (np.max(By_y) + np.min(By_y))/2    
                By_NperSet = math.ceil(float(BySegUnit) / dx_By)
                
                return [dx_By,ByStart_2plot,ByEnd,ByStart_index,BySegNum,Bysegs,ymean_By,By_NperSet]
            
        #plot Bx segments 
        def plotseg_Bx():

            try:
                init = Bxseg_init()
                
    #            dx_Bx = init[0]
    #            BxStart = init[1]
    #            BxStart_index = init[3]
                BxSegNum = init[4]
                Bxsegs_2plot = init[5]
    #                Bxsegs_2cal = init[8]
                ymean_Bx = init[6]
                
                #plot segs
                a.plot(Bxsegs_2plot[0],ymean_Bx,'r.',markersize=10)
                a.plot(Bxsegs_2plot,[ymean_Bx]*(BxSegNum+1),'r|',markersize=15,fillstyle='none')
    #                a.plot(Bxsegs_2cal,[ymean_Bx]*(BxSegNum+1),'b|',markersize=15,fillstyle='none')
                #plot Riemann sum
    #                a.bar(Bx_x[BxStart_index:]-dx_Bx/2,Bx_y[BxStart_index:],width=dx_Bx,alpha=0.2,align='edge',edgecolor='b')
               
                show_canvas(f,self)

            except:
                pass
#                data_format_warn()
                
        #plot By segments
        def plotseg_By():

            try:         
                init = Byseg_init()
                      
    #            dx_By = init[0]
    #            ByStart = init[1]
    #            ByStart_index = init[3]
                BySegNum = init[4]
                Bysegs_2plot = init[5]
#                Bysegs = init[5]
                ymean_By = init[6]
                
                #plot segs
                b.plot(Bysegs_2plot[0],ymean_By,'r.',markersize=10)
                b.plot(Bysegs_2plot,[ymean_By]*(BySegNum+1),'r|',markersize=15,fillstyle='none')
              
                #plot Riemann sum
    #                b.bar(By_x[ByStart_index:]-dx_By/2,By_y[ByStart_index:],width=dx_By,alpha=0.2,align='edge',edgecolor='b')
    #                  
                show_canvas(f,self)

            except:
                pass
#                data_format_warn()
        
        #show canvas
        def show_canvas(f,self):
            #設定canvas圖 加入畫布
            canvas = FigureCanvasTkAgg(f, self)
            canvas.show()
    #        canvas.get_tk_widget().pack(side=tk.BOTTOM,fill=tk.BOTH, expand=True)
            canvas.get_tk_widget().grid(column=0, row=1,rowspan=9, pady=0, sticky = tk.N + tk.S)
            
            #matplotlib 要用 grid的話要用tk.Frame
            toolbarFrame = tk.Frame(self, bg='white')
            toolbarFrame.grid(column=0, row=10,columnspan=1,sticky= tk.W + tk.E + tk.N + tk.S)
            toolbar = NavigationToolbar2TkAgg(canvas, toolbarFrame)
        
        #clear text window
        def clear_text():
            ResultText.delete('1.0', tk.END)
        
        #clear canvas
        def clear_canvas():
            a.clear()
            b.clear()
#            plot_BG_Bx()
#            plot_BG_By()
#            plot_Bx()
#            plot_By()
            fieldUnit = comboBUnit.get()
            axisUnit = comboSegUnit.get()
            plot_bg(fieldUnit,axisUnit)
            self.sw_x = 0
            self.sw_y = 0
            self.sw_reset = 1
#            self.BG_Bx = input_data()
#            self.BG_By = input_data()
#            self.Bx = input_data()
#            self.By = input_data()
            
        #clear segments plot
        def clear_segs():
            a.clear()
            b.clear()
            plot_Bx()
            plot_By()
            
        #plot Background Bx data    
        def plot_BG_Bx():
            #Bx場     
            if type(self.BG_Bx_x) == np.ndarray and type(self.BG_Bx_y) == np.ndarray:
                a.plot(self.BG_Bx_x,self.BG_Bx_y,'C0-') 
    
            fieldUnit = comboBUnit.get()
            axisUnit = comboSegUnit.get()
            plot_bg(fieldUnit,axisUnit)
        
        #plot Background By data
        def plot_BG_By():
            #By場
            if type(self.BG_By_x) == np.ndarray and type(self.BG_By_y) == np.ndarray:
                b.plot(self.BG_By_x,self.BG_By_y,'C0-') 
            
            fieldUnit = comboBUnit.get()
            axisUnit = comboSegUnit.get()
            plot_bg(fieldUnit,axisUnit)
        
        #plot Bx data
        def plot_Bx():
            #Bx場     
            if type(self.Bx_x) == np.ndarray and type(self.Bx_y) == np.ndarray:
                a.plot(self.Bx_x,self.Bx_y,'k.',markersize = 1.5) 
    
            fieldUnit = comboBUnit.get()
            axisUnit = comboSegUnit.get()
            plot_bg(fieldUnit,axisUnit)
        
        #plot By data
        def plot_By():
            #By場
            if type(self.By_x) == np.ndarray and type(self.By_y) == np.ndarray:
                b.plot(self.By_x,self.By_y,'k.',markersize = 1.5) 
            
            fieldUnit = comboBUnit.get()
            axisUnit = comboSegUnit.get()
            plot_bg(fieldUnit,axisUnit)
        
        #plot canvas background
        def plot_bg(fieldUnit,axisUnit):
            
            a.set_ylabel('Bx(' + fieldUnit + ')')
            a.grid(color = 'gray',linestyle='--')
            b.set_xlabel('Z axis(' + axisUnit + ')')
            b.set_ylabel('By(' + fieldUnit + ')')
           
            b.grid(color = 'gray',linestyle='--')
#            b.autoscale(False)
            #建立畫布
            show_canvas(f,self)
            
        #integral calculation and print result    
        def calculate():
#            text = '                       \n' 
#            ResultText.insert(tk.END,"{:>8d} %s\t %s\t %s\t %s\t %s\t %s\n" % ("Index","N_perSet","Ix(gauss-cm)","Index","N_perSet","Iy(gauss-cm)"))
            fieldUnit = comboBUnit.get()
            axisUnit = comboSegUnit.get()
            
            ResultText.insert(tk.END,"{:>12s}{:>12s}{:>12s}{:>12s}{:>12s}{:>12s}\n".format("Index","N_perSet","Ix(" + fieldUnit[0] + '-' + axisUnit + ")","Index","N_perSet","Iy(" + fieldUnit[0] + '-' + axisUnit + ")"))
            #            ResultText.insert(tk.END,text)
            try:
                Bx_init = Bxseg_init()
                BxStart_index = Bx_init[3]
                dx_Bx = Bx_init[0]
                Bxsegs = Bx_init[5]
                sx_a = self.Bx_x[BxStart_index:]
                sy_a = self.Bx_y[BxStart_index:]
    
                By_init = Byseg_init()
                ByStart_index = By_init[3]
                dx_By = By_init[0]
                Bysegs = By_init[5]
                sx_b = self.By_x[ByStart_index:]
                sy_b = self.By_y[ByStart_index:]
                  
                Ix_seg = Riemann_sum(dx_Bx,sx_a,sy_a,Bxsegs)
    #            print('a')
                Iy_seg = Riemann_sum(dx_By,sx_b,sy_b,Bysegs)
    #            print('b')
                #補差距
                n = max([len(Ix_seg),len(Iy_seg)])
                
                s=' ';
    
                for i in range(n):
    
                    try:
                        ResultText.insert(tk.END,"{:>12s}{:>12.1f}{:>12.3f}".format(str(i+1),len(Ix_seg[i]),sum(Ix_seg[i])))
                    except:
                        ResultText.insert(tk.END,"{:>12s}{:>12s}{:>12s}".format(s,s,s))  
    #                for n,i in enumerate(Iy_seg):
                    try:
                        ResultText.insert(tk.END,"{:>12s}{:>12.1f}{:>12.3f}\n".format(str(i+1),len(Iy_seg[i]),sum(Iy_seg[i])))
                    except:
                        ResultText.insert(tk.END,"\n")
            except:
                pass
            
##                print(i+1)
#                print(str(i) + '        ' + str(sum(Iy_seg[i]) + '\n'))
#                ResultText.insert(tk.END, str(i) + '        ' + str(sum(Ix_seg[i]))+ \
#                                  '        ' + str(i) + '        ' + str(sum(Iy_seg[i]) + '\n'))
#       #integral calculation 
#        def Riemann_sum(dx,y,NperSet):
#        
#            #integral
#            
##            I = dx_Bx * Bx_y
##            NperSet = Bx_NperSet
#            I = dx * y
#            Q = divmod(len(I) , NperSet)[0]
#            R = divmod(len(I) , NperSet)[1]
#            
#            if R == 0:
#                I_segs = np.split(I,Q)[:-1]
#            
#            #若不能整除，求餘數再重分割
#            else: 
#                
#                div_segs = I[:(len(I)-R)]
#                I_segs = np.split(div_segs,Q)
##                I_seg.append(I[(len(I)-R):])
#                
#                
#            return I_segs
        
        #integral calculation 
        def Riemann_sum(dx,x,y,segs):
            #integral
            I = dx * y
#            x_segs = []
            I_segs = []
            for i in range(len(segs) - 1):
                index1 = np.where(x == find_2adjacent(x, segs[i],'Upper','former'))[0][0]
                index2 = np.where(x == find_2adjacent(x, segs[i+1],'Lower','later'))[0][0]
#                x_seg = x[index1:index2 + 1]
#                x_segs.append(x_seg)
                I_seg = I[index1:index2 + 1]
                I_segs.append(I_seg)
#                print(I_seg)
            
            return I_segs
     
        #data parse
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
        
        #This is where we lauch the file manager bar.
        def OpenFile():
            self.sw_reset = 0
            name = askopenfilename(
                                   filetypes =(("Text File", "*.txt"),("All Files","*.*")),
                                   title = "Choose a file."
                                   )
#            print(name)
            #Using try in case user types in unknown file or closes without choosing a file.
            try:
                df = pd.read_csv(name,sep = '\t')
                df = format_data(df)
#                print(np.array(df[df.columns[0]]))
#                print(np.array(df[df.columns[1]]))
#                print(df)
                return [np.array(df[df.columns[0]]),np.array(df[df.columns[1]])]
#                with open(name,'r') as UseFile:
#                    print(UseFile.read())
            except:
                print("No file exists")
                
        #This is where we lauch the file manager bar.
        def SaveFile():
            name = asksaveasfilename(
#                    initialdir = "/",
                    title = "Save file",
                    filetypes = (("Text File","*.txt"),("All Files","*.*"))
                    )
            
#            print(name)
            
            text = ResultText.get(1.0,tk.END)
            with open(name + ".txt", "a") as f:
                f.write(text)
                
            f.close()
        
        def OpenBG_Bx():
            try:
                data = OpenFile()
                self.BG_Bx.set_xval(data[0])
                self.BG_Bx.set_yval(data[1])
                self.BG_Bx_x = self.BG_Bx.get_xval()
                self.BG_Bx_y = self.BG_Bx.get_yval()
                plot_BG_Bx()
            except:
                pass
            
        def OpenBG_By():
            try:
                data = OpenFile()
                self.BG_By.set_xval(data[0])
                self.BG_By.set_yval(data[1])
                self.BG_By_x = self.BG_By.get_xval()
                self.BG_By_y = self.BG_By.get_yval()
                plot_BG_By()
#                plot_init()
            except:
                pass
            
        def OpenBx():
            try:
                data = OpenFile()
                self.Bx.set_xval(data[0])
                self.Bx.set_yval(data[1])
                self.Bx_x = self.Bx.get_xval()
                self.Bx_y = self.Bx.get_yval()
                
    #            print(Bx.get_xval(),Bx.get_yval())
                plot_Bx()
#            Bx_init()
            except:
                pass
        
        def OpenBy():
            try:
                data = OpenFile()
                self.By.set_xval(data[0])
                self.By.set_yval(data[1])
                self.By_x = self.By.get_xval()
                self.By_y = self.By.get_yval()
                plot_By()
                
            except:
                pass
        
        def cutoff_BG_Bx():
            #可能會重複減 要檢查
            if self.sw_reset == 1 or type(self.Bx_y) == int or type(self.BG_Bx_y) == int:
                showinfo("Warning", "Please choose data files including BG files.")
                
            elif self.sw_x == 0 and type(self.Bx_y) != int and type(self.BG_Bx_y) != int:
                self.Bx_y = self.Bx_y - self.BG_Bx_y
                a.clear()
                plot_Bx() 
                self.sw_x = 1
        
            else:
                showinfo("Warning", "BG_Bx was cut off already.")   
                
        def cutoff_BG_By():
            #可能會重複減 要檢查
            if self.sw_reset == 1 or type(self.By_y) == int or type(self.By_y) == int:
                showinfo("Warning", "Please choose data files including BG files.")
                
            elif self.sw_y == 0 and type(self.By_y) != int and type(self.BG_By_y) != int:
                self.By_y = self.By_y - self.BG_By_y
                b.clear()
                plot_By() 
                self.sw_y = 1
   
            else:
                showinfo("Warning", "BG_By was cut off already.")   
        
        
        #Create widgets
        tk.Frame.__init__(self, parent,bg='white')
        title = tk.Label(self,bg='white', text="Bx,By field distribution.", font = "Calibri 18 bold italic")
#        title.pack(pady=10,padx=10)
        title.grid(column=0, row=0,padx=10,sticky= tk.W + tk.E + tk.N + tk.S)
        
        label1 = tk.Label(self,bg='white', text="Choose background file:", font = "Calibri 12 bold")
        label1.grid(column=1,columnspan=2, row=0, padx=10,pady=5, sticky=tk.W)
        
        label6 = tk.Label(self,bg='white', text="Choose raw data file:", font = "Calibri 12 bold")
        label6.grid(column=3,columnspan=2, row=0, padx=10,pady=5, sticky=tk.W)
        
        label2 = tk.Label(self,bg='white',text="Set x0 for Bx:", font = "Calibri 12 bold")
        label2.grid(column=1, row=4, padx=10, pady=5, sticky=tk.W)
        
        label3 = tk.Label(self,bg='white',text="Set x0 for By:", font = "Calibri 12 bold")
        label3.grid(column=1, row=5, padx=10, pady=5, sticky=tk.W)
    
        label7 = tk.Label(self,bg='white',text="Select B-field Unit:", font = "Calibri 12 bold")
        label7.grid(column=1, row=3, padx=10, pady=5, sticky=tk.W)
        
        label4 = tk.Label(self,bg='white',text="Set Bx segments:", font = "Calibri 12 bold")
        label4.grid(column=3, row=4, padx=10, pady=5, sticky=tk.W)
        
        label5 = tk.Label(self,bg='white',text="Set By segments:", font = "Calibri 12 bold")
        label5.grid(column=3, row=5, padx=10, pady=5, sticky=tk.W)
        
        label8 = tk.Label(self,bg='white',text="Select axis Unit:", font = "Calibri 12 bold")
        label8.grid(column=3, row=3, padx=10, pady=5, sticky=tk.W)
       
        #drop list
        comboBUnit = ttk.Combobox(self, 
                            values=[
                                    "Gauss", 
                                    "Tesla",
                                    ],
                            width = 12)
        comboBUnit.grid(column=2, row=3, padx=10,pady=5, sticky=tk.W)
        comboBUnit.current(0)
        
        comboSegUnit = ttk.Combobox(self, 
                            values=[
                                    "mm", 
                                    "cm",
                                    ],
                            width = 12)
        comboSegUnit.grid(column=4, row=3, padx=10,pady=5, sticky=tk.W)
        comboSegUnit.current(1)
 
#        entryFile = tk.Entry(self,width=24,borderwidth = 2)
        entryBxin = tk.Entry(self,width=14,borderwidth=2)
        entryByin = tk.Entry(self,width=14,borderwidth=2)
        entryBxSegments = tk.Entry(self,width=14,borderwidth=2)
        entryBySegments = tk.Entry(self,width=14,borderwidth=2)
        
#        entryFile.grid(column=2,columnspan = 1 , row=0, padx=10, pady=5, sticky=tk.W)
        entryBxin.grid(column=2, row=4, padx=10, pady=5, sticky=tk.W)
        entryByin.grid(column=2, row=5, padx=10, pady=5, sticky=tk.W)
        entryBxSegments.grid(column=4, row=4, padx=10, pady=5, sticky=tk.W)
        entryBySegments.grid(column=4, row=5, padx=10, pady=5, sticky=tk.W)
        
#        label1.pack(pady=10,padx=100,side = 'right', anchor='ne')
#        #tkk的style要另外設定
        style = ttk.Style()
        style.configure("TButton", background="white",font = "Calibri 12")
#        
        button0 = ttk.Button(self, text="Open Bx", width=12, command = OpenBG_Bx)
        button0.grid(column=1, row=1, padx=10, pady=5, sticky=tk.W)
        
        button7 = ttk.Button(self, text="Open By", width=12, command = OpenBG_By)
        button7.grid(column=2, row=1, padx=10, pady=5, sticky=tk.W)
        
        button8 = ttk.Button(self, text="Open Bx", width=12, command = OpenBx)
        button8.grid(column=3, row=1, padx=10, pady=5, sticky=tk.W)
        
        button9 = ttk.Button(self, text="Open By", width=12, command = OpenBy)
        button9.grid(column=4, row=1, padx=10, pady=5, sticky=tk.W)
        
        button10 = ttk.Button(self, text="Cut off BG_Bx",width=12, command = cutoff_BG_Bx)
        button10.grid(column=3, row=2, padx=10, pady=5, sticky=tk.W)
        
        button11 = ttk.Button(self, text="Cut off BG_By",width=12, command = cutoff_BG_By)
        button11.grid(column=4, row=2, padx=10, pady=5, sticky=tk.W)
        
        
#        button1 = ttk.Button(self, text="Plot", command = plotseg_Bx)
#        button1.grid(column=1, row=5, padx=10, pady=5, sticky=tk.W)
#        
#       button1.grid(row=0,column=0)
        
        button2 = ttk.Button(self, text="Clear Plot",width=12, command = clear_canvas)
        button2.grid(column=3, row=7, padx=10, pady=5, sticky=tk.W)
       
        button13 = ttk.Button(self, text="Clear segs",width=12, command = clear_segs)
        button13.grid(column=3, row=6, padx=10, pady=5, sticky=tk.W)
        
        button12 = ttk.Button(self, text="Plot Bx seg",width=12, command = plotseg_Bx)
        button12.grid(column=1, row=6, padx=10, pady=5, sticky=tk.W)
      
        button13 = ttk.Button(self, text="Plot By seg",width=12, command = plotseg_By)
        button13.grid(column=2, row=6, padx=10, pady=5, sticky=tk.W)
        
        button3 = ttk.Button(self, text="Calculate",width=12, command = calculate)
        button3.grid(column=1, row=7, padx=10, pady=5, sticky=tk.W)
      
        button4 = ttk.Button(self, text="Save as",width=12, command = SaveFile)
        button4.grid(column=4, row=7, padx=10, pady=5, sticky=tk.W)
        
        button5 = ttk.Button(self, text="Smart plot",width=12, )
        button5.grid(column=4, row=6, padx=10, pady=5, sticky=tk.W)
        
        button6 = ttk.Button(self, text="Clear text",width=12, command = clear_text)
        button6.grid(column=2, row=7, padx=10, pady=5, sticky=tk.W)
        
        label6 = tk.Label(self,bg='white',text="Results:", font = "Calibri 12")
        label6.grid(column=1, row=8, padx=10, pady=5, sticky=tk.W)

        ResultText = tk.Text(self,width=20,borderwidth=2)
        ResultText.grid(column=1,columnspan=4,row=9,padx=10, pady=5,sticky= tk.W + tk.E + tk.N + tk.S)
        
        #cut off switch
        self.sw_x = 0
        self.sw_y = 0
        
        #reset switch
        self.sw_reset = 0
#
        #定義畫圖data
        f = Figure(figsize=(7,3), dpi=100)
        #Bx場
#        t = np.linspace(0, 3,31)
        
        #BG
        self.BG_Bx = input_data()
        self.BG_Bx_x = self.BG_Bx.get_xval()
        self.BG_Bx_y = self.BG_Bx.get_yval()
        
        self.BG_By = input_data()
        self.BG_By_x = self.BG_By.get_xval()
        self.BG_By_y = self.BG_By.get_yval()
        
        #Bx場
        self.Bx = input_data()
        self.Bx_x = self.Bx.get_xval()
        self.Bx_y = self.Bx.get_yval()
        a = f.add_subplot(211,fc = 'white')
  
        #By場
        self.By = input_data()
        self.By_x = self.By.get_xval()
        self.By_y = self.By.get_yval()
        b = f.add_subplot(212,fc = 'white')
        
        fieldUnit = comboBUnit.get()
        axisUnit = comboSegUnit.get()
        plot_bg(fieldUnit,axisUnit)
        
#        first_plot()
        
def main():
    app = IntegralAnalysis()
    app.mainloop()

if __name__== "__main__":
    main()            

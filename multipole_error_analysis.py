# -*- coding: utf-8 -*-
"""
Created on Thu Jul 11 15:22:30 2019

@author: Administrator
"""
#import matplotlib
#matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
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
        self._filename = ''
        self._x = 0
        self._Ix = 0
        self._Iy = 0
          
    def get_Ix_val(self):
        return self._Ix

    def get_Iy_val(self):
        return self._Iy
    
    def get_xval(self):
        return self._x
    
    def get_filename(self):
        return self._filename
    
    def set_Ix_val(self,m):
        self._Ix = m
    
    def set_Iy_val(self,m):
        self._Iy = m

    def set_xval(self,m):
        self._x = m
    
    def set_filename(self,m):
        self._filename = m
            
        
class IntegralAnalysis(tk.Tk):

    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)

#        tk.Tk.iconbitmap(self, default="clienticon.ico")
        tk.Tk.wm_title(self, "Multipole error analysis for stretched wire measurement")
        
        
        container = tk.Frame(self)
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
        def set_order_remind():
            showinfo("Warning", "Please set order for fitting!")
        
        def nondivisible_warn():
            showinfo("Warning", "Please set a value which makes it divisible.")
        
        def data_format_warn():
            showinfo("Warning", "Please make sure the format of data is correct.")
            
        def get_data(filename):
            #輸入檔名並解析成dataframe format
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
        
        #回傳fitting係數
        def polyfit_coeff(x,y,order):
            #檢查輸入資料格式
            
                #polyfit
            coeff = np.polyfit(x,y,order)      
            return coeff
        
        #回傳fitting後的data
        def fitting_data(x,coeff):
            
            fc = np.poly1d(coeff)
            fy = fc(x)  #fitting y
            
            return fy
        
        
        def plot_fit(x,y1,y2):
            
            if entryFitOrder.get() == '':
                set_order_remind()
            else:
                order = int(entryFitOrder.get())
                Ix_coeff = polyfit_coeff(x,y1,order)
                a.plot(np.array(self.x),np.array(fitting_data(x,Ix_coeff)),'r.--') 
                
                Iy_coeff = polyfit_coeff(x,y2,order)
                b.plot(np.array(self.x),np.array(fitting_data(x,Iy_coeff)),'r.--') 
                
                plot_bg()
                
                return [Ix_coeff,Iy_coeff]
        
        def show_canvas(f,self):
            #設定canvas圖 加入畫布
            canvas = FigureCanvasTkAgg(f, self)
            canvas.show()
    #        canvas.get_tk_widget().pack(side=tk.BOTTOM,fill=tk.BOTH, expand=True)
            canvas.get_tk_widget().grid(column=0, row=1,rowspan=8, pady=0, sticky = tk.N + tk.S)
            
            #matplotlib 要用 grid的話要用tk.Frame
            toolbarFrame = tk.Frame(self, bg='white')
            toolbarFrame.grid(column=0, row=10,columnspan=1,sticky= tk.W + tk.E + tk.N + tk.S)
            toolbar = NavigationToolbar2TkAgg(canvas, toolbarFrame)
        
        def clear_text():
            ResultText.delete('1.0', tk.END)
        
        def clear_canvas():
            a.clear()
            b.clear()
#            plot_BG_Ix()
#            plot_BG_Iy()
#            plot_Ix()
#            plot_Iy()
            plot_bg()
            self.sw_x = 0
            self.sw_y = 0
            
            
        def plot_BG():
            #Ix場     
            if type(self.BG_x) == np.ndarray and type(self.BG_Ix) == np.ndarray:
                a.plot(self.BG_x,self.BG_Ix,'C0.-') 
    
            if type(self.BG_x) == np.ndarray and type(self.BG_Iy) == np.ndarray:
                b.plot(self.BG_x,self.BG_Iy,'C0.-') 
            
            plot_bg()
        
        def plot_I():
            #Ix場     
            if type(self.x) == np.ndarray and type(self.Ix) == np.ndarray:
                a.plot(self.x,self.Ix,'k.-') 
    
            #Iy場
            if type(self.x) == np.ndarray and type(self.Iy) == np.ndarray:
                b.plot(self.x,self.Iy,'k.-') 
            
            plot_bg()
        
        def plot_bg():
            
            a.set_ylabel('Ix(Gauss-cm)')
            a.grid(color = 'gray',linestyle='--')
            b.set_xlabel('X axis(cm)')
            b.set_ylabel('Iy(Gauss-cm)')
           
            b.grid(color = 'gray',linestyle='--')
#            b.autoscale(False)
            #建立畫布
            show_canvas(f,self)
            
        def calculate():
#            text = '                       \n' 
            if entryFitOrder.get() == '':
                set_order_remind()

            else:
                try:
                    ResultText.insert(tk.END,"Background file: \n")
                    ResultText.insert(tk.END,self.BG_filename + "\n\n")
                    ResultText.insert(tk.END,"Measurment data file: \n")
                    ResultText.insert(tk.END,self.I_filename + "\n\n")
                except:
                    showinfo("Warning", "You must select BG and measurment file to calculate.")
                
                ResultText.insert(tk.END,"{:>12s}{:>20s}{:>12s}{:>20s}\n".format("Index","Ix_coeff(G/cm^n-1)","Index","Iy_coeff(G/cm^n-1)"))
                [Ix_coeff,Iy_coeff] = plot_fit(self.x,self.Ix,self.Iy)
                
                Ix_coeff = Ix_coeff[::-1] 
                Iy_coeff = Iy_coeff[::-1]
                
                s=' ';
                
                
                for i in range(len(Ix_coeff)):
    
                    try:
                        ResultText.insert(tk.END,"{:>12s}{:>20.3f}".format(str(i),Ix_coeff[i]))
                    except:
                        ResultText.insert(tk.END,"{:>12s}{:>20s}".format(s,s))  
    #                for n,i in enumerate(Iy_seg):
                    try:
                        ResultText.insert(tk.END,"{:>12s}{:>20.3f}\n".format(str(i),Iy_coeff[i]))
                    except:
                        ResultText.insert(tk.END,"\n")
    ##                print(i+1)
    #                print(str(i) + '        ' + str(sum(Iy_seg[i]) + '\n'))
    #                ResultText.insert(tk.END, str(i) + '        ' + str(sum(Ix_seg[i]))+ \
#                                  '        ' + str(i) + '        ' + str(sum(Iy_seg[i]) + '\n'))
        
        #This is where we lauch the file manager bar.
        def OpenFile():
            name = askopenfilename(
                                   filetypes =(("Text File", "*.txt"),("All Files","*.*")),
                                   title = "Choose a file."
                                   )
            
#            print(name)
            #Using try in case user types in unknown file or closes without choosing a file.
            try:
                df = get_data(name)
                x = df['Position(cm)']
                Ix = df['Ix(G-cm)']
                Iy = df['Iy(G-cm)']              
                return [np.array(x),np.array(Ix),np.array(Iy),name]
            
#                with open(name,'r') as UseFile:
#                    print(UseFile.read())
            except:
                pass
                
        #This is where we lauch the file manager bar.
        def SaveFile():
            name = asksaveasfilename(
#                    initialdir = "/",
                    title = "Save file",
                    filetypes = (("Text File","*.txt"),("All Files","*.*"))
                    )
            
#            print(name)
            
            text = ResultText.get(1.0,tk.END)
            
            try:
                if name.split('.')[1] == 'txt':
                    name == name.split('.')[0]
            except:
                name = name + '.txt'
                
            with open(name, "w") as f:
                f.write(text)
                
            f.close()
    
        def OpenBG_I():
            try:
                data = OpenFile()
                BG_I.set_xval(data[0])
                BG_I.set_Ix_val(data[1])
                BG_I.set_Iy_val(data[2])
                BG_I.set_filename(data[3])
                
                self.BG_x = BG_I.get_xval()
                self.BG_Ix = BG_I.get_Ix_val()
                self.BG_Iy = BG_I.get_Iy_val()
                self.BG_filename = BG_I.get_filename()   
            
                plot_BG()
                
            except:
                pass
            
        def OpenI():
            try:
                data = OpenFile()
                I.set_xval(data[0])
                I.set_Ix_val(data[1])
                I.set_Iy_val(data[2])
                I.set_filename(data[3])
                
                self.x = I.get_xval()
                self.Ix = I.get_Ix_val()
                self.Iy = I.get_Iy_val()
                self.I_filename = I.get_filename() 
                
                plot_I()
                
            except:
                pass

        
        def cutoff_BG_I():
            #可能會重複減 要檢查
            if self.sw_x == 0:
                self.Ix = self.Ix - self.BG_Ix
                self.Iy = self.Iy - self.BG_Iy
                
                a.clear()
                b.clear()
                plot_I()
                self.sw_x = 1
            
            else:
                showinfo("Warning", "BG_Ix was cut off already.")   
        
        def clear_fitting():
            a.clear()
            b.clear()
            plot_I()
                     
            
        #Create widgets
        tk.Frame.__init__(self, parent,bg='white')
        title = tk.Label(self,bg='white', text="Ix,Iy distribution on X-axis.", font = "Calibri 18 bold italic")
#        title.pack(pady=10,padx=10)
        title.grid(column=0, row=0,padx=10,sticky= tk.W + tk.E + tk.N + tk.S)
        
        label1 = tk.Label(self,bg='white', text="Choose background file:", font = "Calibri 12 bold")
        label1.grid(column=1, row=0, padx=10,pady=5, sticky=tk.W)
        
        label6 = tk.Label(self,bg='white', text="Choose raw data file:", font = "Calibri 12 bold")
        label6.grid(column=3, row=0, padx=10,pady=5, sticky=tk.W)
        
        label2 = tk.Label(self,bg='white',text="Set fitting order:", font = "Calibri 12 bold")
        label2.grid(column=1, row=3, padx=10, pady=5, sticky=tk.W)

        label3 = tk.Label(self,bg='white',text="Set normalized range(mm):", font = "Calibri 12 bold")
        label3.grid(column=3, row=3, padx=10, pady=5, sticky=tk.W)
        
        
#        entryFile = tk.Entry(self,width=24,borderwidth = 2)
        entryFitOrder = tk.Entry(self,width=12,borderwidth=2)
        entryNorm = tk.Entry(self,width=12,borderwidth=2)

        
#        entryFile.grid(column=2,columnspan = 1 , row=0, padx=10, pady=5, sticky=tk.W)
        entryFitOrder.grid(column=2, row=3, padx=10, pady=5, sticky=tk.W)
        entryNorm.grid(column=4, row=3, padx=10, pady=5, sticky=tk.W)
        
        
#        label1.pack(pady=10,padx=100,side = 'right', anchor='ne')
#        #tkk的style要另外設定
        style = ttk.Style()
        style.configure("TButton", background="white",font = "Calibri 12")
#        
        button0 = ttk.Button(self, text="Open BG_I", command = OpenBG_I)
        button0.grid(column=1, row=1, padx=10, pady=5, sticky=tk.W)
           
        button8 = ttk.Button(self, text="Open I", command = OpenI)
        button8.grid(column=3, row=1, padx=10, pady=5, sticky=tk.W)
        
        button10 = ttk.Button(self, text="Cut off BG_I",command = cutoff_BG_I)
        button10.grid(column=3, row=2, padx=10, pady=5, sticky=tk.W)
        
        
        button2 = ttk.Button(self, text="Clear Plot",command = clear_canvas)
        button2.grid(column=3, row=5, padx=10, pady=5, sticky=tk.W)
        
        button1 = ttk.Button(self, text="Clear Fitting",command = clear_fitting)
        button1.grid(column=3, row=6, padx=10, pady=5, sticky=tk.W)

        button3 = ttk.Button(self, text="Calculate",command = calculate)
        button3.grid(column=1, row=5, padx=10, pady=5, sticky=tk.W)
      
        button4 = ttk.Button(self, text="Save as",command = SaveFile)
        button4.grid(column=4, row=5, padx=10, pady=5, sticky=tk.W)
    
        
        button6 = ttk.Button(self, text="Clear text", command = clear_text)
        button6.grid(column=2, row=5, padx=10, pady=5, sticky=tk.W)
        
        label6 = tk.Label(self,bg='white',text="Results:", font = "Calibri 12")
        label6.grid(column=1, row=7, padx=10, pady=5, sticky=tk.W)

        ResultText = tk.Text(self,width=20,borderwidth=2)
        ResultText.grid(column=1,columnspan=4,row=8,padx=10, pady=5,sticky= tk.W + tk.E + tk.N + tk.S)
        
        #cut off switch
        self.sw_x = 0
        self.sw_y = 0
#
        #定義畫圖data
        f = Figure(figsize=(7,3), dpi=100)
        #Ix場
#        t = np.linspace(0, 3,31)
        
        #BG
        BG_I = input_data()
        self.BG_x = BG_I.get_xval()
        self.BG_Ix = BG_I.get_Ix_val()
        self.BG_Iy = BG_I.get_Iy_val()
     
        #Ix場
        I = input_data()
        self.x = I.get_xval()
        self.Ix = I.get_Ix_val()
        self.Iy = I.get_Iy_val()
        a = f.add_subplot(211,fc = 'white')
        b = f.add_subplot(212,fc = 'white')
        
        plot_bg()
#        first_plot()
        
app = IntegralAnalysis()
app.mainloop()
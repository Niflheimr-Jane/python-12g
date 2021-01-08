import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
from tkinter import *
import sys
from os import listdir
from os.path import isdir
from PIL import ImageTk, Image
import argparse
import codecs
import copy
import re
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

scale = 1
W, H = 800, 600
exercise = ['久坐(辦公室工作、沒有運動習慣)',     # 1
            '輕度(運動1-2天/週)',               # 2
            '中度(運動3-5天/週)',               # 3
            '高度(運動6-7天/週)',               # 4
            '極高度(運動員等級，每天運動2次)']   # 5

KCAL = dict()
KCAL['milk'] = 50

class Data:
    def __init__(self, database):
        self.name = None # type: string
        self.height = None # type: float
        self.weight = None # type: float
        self.gender = None # type: int symbol: 0->female, 1->male
        self.age = None # type: int
        self.exercise = None # type: int symbol: reference the list 'exercise' above

        FOOD = dict()        
        for d in listdir(database):
            for f in listdir(f'{database}/{d}'):
                ss = f.split('.J')[0]
                FOOD[ss] = 0

        self.breakfast = copy.deepcopy(FOOD)
        self.lunch = copy.deepcopy(FOOD)
    
    def __str__(self):
        ss = f"Name: {self.name} Gender: {self.gender} Age: {self.age}\n"
        ss += f"Height: {self.height} Weight: {self.weight}\n"
        ss += f"Exercise: {self.exercise}\n"
        ss += "Breakfast:\n"
        for idx, (key,value) in enumerate(self.breakfast.items()):
            if value != 0:
                ss += f"{key}: {value}\n"

        ss += "Lunch:\n"
        for idx, (key,value) in enumerate(self.lunch.items()):
            if value != 0:
                ss += f"{key}: {value}\n"
        return ss



class Item(tk.Frame):
    def __init__(self, master, name, idx, data):
        tk.Frame.__init__(self, master)
        self.meal = master.meal
        self.configure(bg='white')
        self.data = data
        self.mainFrame = master.mainFrame
        textSize = 18
        fontStyle = tkFont.Font(family="Noto Sans Mono CJK TC", size=textSize, weight='bold')
 
        self.labelName = tk.Label(self, text=name, font=fontStyle, bg='white')
        self.labelName.pack(side='left')
        amount = list(range(100))
        self.comb = ttk.Combobox(self, width=5, values=amount, font=fontStyle)
        self.comb.current(0)
        self.comb.bind('<<ComboboxSelected>>', self.modified)
        self.comb.pack(side='right')

    def modified(self, event):
        if self.meal == 'breakfast':
            self.data.breakfast[self.labelName.cget('text')] = int(self.comb.get())
            self.mainFrame.listbox.delete(0,END)
            for key, value in self.data.breakfast.items():
                if value != 0:
                    self.mainFrame.listbox.insert(END, f'{key}:{value}')
        else:
            self.data.lunch[self.labelName.cget('text')] = int(self.comb.get())
            self.mainFrame.listbox.delete(0,END)
            for key, value in self.data.lunch.items():
                if value != 0:
                    self.mainFrame.listbox.insert(END, f'{key}:{value}')

class Menu(tk.Frame):
    def __init__(self, master, cat):
        tk.Frame.__init__(self, master)
        self.master = master
        self.data = master.data
        self.meal = master.meal
        self.mainFrame = master
        self.configure(bg='white')
        canvas = tk.Canvas(self, bg='white')
        scrollbar = tk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = tk.Frame(canvas, bg='white')
        self.scrollable_frame.pack(side=LEFT, fill=X, expand=True)
        self.scrollable_frame.meal = self.meal
        self.scrollable_frame.mainFrame = master
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor=NW)
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side=LEFT,fill=X, expand=True)
        scrollbar.pack(side=RIGHT,fill=Y)
        
        files = listdir(f'{database}/{cat}')
        self.items = list()
        for idx, f in enumerate(files):
            ss = f.split('.J')[0]
            item = Item(self.scrollable_frame, ss, idx, self.data)
            if self.meal == 'breakfast':
                item.comb.current(self.data.breakfast[ss])
            else:
                item.comb.current(self.data.lunch[ss])
            item.pack(side=TOP, fill=X, expand=True)
            self.items.append(item)

    def update(self):
        for item in self.items:
            print(item.labelName.cget('text'), item.comb.get())

class GUI(tk.Tk):
    def __init__(self, data):
        tk.Tk.__init__(self)
        self.data = data
        self.frame = None
        self.title('2020 NYMU Final Project No.12')
        self.geometry(f'{W}x{H}')
        self.configure(background='white')
        self.resizable(0, 0)
        self.switch_frame(StartPage)
    
    def switch_frame(self, frame_class, meal=None):
        if meal is not None:
            new_frame = frame_class(self, meal)
        else:
            new_frame = frame_class(self)
        if self.frame is not None:
            self.frame.destroy()
        self.frame = new_frame
        self.frame.pack(fill=BOTH,expand=True)

class StartPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.data = master.data
        self.master = master
        self.configure(bg='white')

        textSize = 18
        fontStyle = tkFont.Font(family="Noto Sans Mono CJK TC", size=textSize, weight='bold')
        
        frame = tk.Frame(self, bg='white')
        frame.pack(fill=BOTH, expand=True, padx=120, pady=100)

        frameName = tk.Frame(frame, bg='white')
        frameName.pack(side=TOP, anchor=NW)
        labelName = tk.Label(frameName, text="使用者姓名：", font=fontStyle, bg='white')
        labelName.pack(side='left')
        self.textName = tk.Text(frameName, width=10, height=1, bg='#F2F2F2', font=fontStyle)
        self.textName.pack(side='left')

        frameH = tk.Frame(frame, bg='white')
        frameH.pack(side=TOP, anchor=NW)
        labelH = tk.Label(frameH, text="身高：", font=fontStyle, bg='white')
        labelH.pack(side='left')
        self.textH = tk.Text(frameH, width=10, height=1, bg='#F2F2F2', font=fontStyle)
        self.textH.pack(side='left')

        frameW = tk.Frame(frame, bg='white')
        frameW.pack(side=TOP, anchor=NW)
        labelW = tk.Label(frameW, text="體重：", font=fontStyle, bg='white')
        labelW.pack(side='left')
        self.textW = tk.Text(frameW, width=10, height=1, bg='#F2F2F2', font=fontStyle)
        self.textW.pack(side='left')

        frameS = tk.Frame(frame, bg='white')
        frameS.pack(side=TOP, anchor=NW)
        labelS = tk.Label(frameS, text="生理性別：", font=fontStyle, bg='white')
        labelS.pack(side='left')
        self.combS = ttk.Combobox(frameS, width=5, values=['男性','女性'], font=fontStyle)
        self.combS.pack(side='left')

        ages = list(range(1,100))
        frameA = tk.Frame(frame, bg='white')
        frameA.pack(side=TOP, anchor=NW)
        labelA = tk.Label(frameA, text="年齡：", font=fontStyle, bg='white')
        labelA.pack(side='left')
        self.combA = ttk.Combobox(frameA, width=5, values=ages, font=fontStyle)
        self.combA.pack(side='left')


        frameE = tk.Frame(frame, bg='white')
        frameE.pack(side=TOP, anchor=NW)
        labelE = tk.Label(frameE, text="運動習慣：", font=fontStyle, bg='white')
        labelE.pack(side='left')
        self.combE = ttk.Combobox(frameE, values=exercise, font=fontStyle)
        self.combE.pack(side='left')

        
        buttonNext = tk.Button(frame, text="下一步", bg='#2E75B6', fg='white', font=fontStyle, command=lambda: [self.record(), master.switch_frame(PageMeal, 'breakfast')])
        buttonNext.pack(side=TOP, anchor=SE)
    
    def record(self):
        self.data.name = self.textName.get(1.0,END).strip()
        self.data.height = float(self.textH.get(1.0,END).strip())
        self.data.weight = float(self.textW.get(1.0,END).strip())
        if self.combS.get().find('男') != -1:
            self.data.gender = 1
        else:
            self.data.gender = 0
        self.data.age = int(self.combA.get().strip())
        self.data.exercise = exercise.index(self.combE.get().strip()) + 1
        
class PageMeal(tk.Frame):
    def __init__(self, master, meal):
        tk.Frame.__init__(self, master)
        self.data = master.data
        self.meal = meal
        self.master = master
        self.menu = None
        self.frameNext = None
        self.frameCh = None
        self.listbox = None
        self.configure(bg='white')

        textSize = 18
        fontStyle = tkFont.Font(family="Noto Sans Mono CJK TC", size=textSize, weight='bold')

        frameBtn = tk.Frame(self, bg='white')
        frameBtn.pack(side=TOP, fill=Y, pady=10)
        if self.meal == 'breakfast':
            ss = "今日早餐："
        else:
            ss = "今日午餐："
        labelBtn = tk.Label(frameBtn, text=ss, font=fontStyle, bg='white')
        labelBtn.pack(side=LEFT)

        buttonTmp = tk.Button(frameBtn, text='奶類', bg='#D9D9D9', fg='black', font=fontStyle, command=lambda: self.switch_frame(Menu, '奶類'))
        buttonTmp.pack(side='right',padx=3)
        buttonTmp = tk.Button(frameBtn, text='穀飲', bg='#D9D9D9', fg='black', font=fontStyle, command=lambda: self.switch_frame(Menu, '穀飲'))
        buttonTmp.pack(side='right',padx=3)
        buttonTmp = tk.Button(frameBtn, text='飯類', bg='#D9D9D9', fg='black', font=fontStyle, command=lambda: self.switch_frame(Menu, '飯類'))
        buttonTmp.pack(side='right',padx=3)
        buttonTmp = tk.Button(frameBtn, text='麵包', bg='#D9D9D9', fg='black', font=fontStyle, command=lambda: self.switch_frame(Menu, '麵包'))
        buttonTmp.pack(side='right',padx=3)
        buttonTmp = tk.Button(frameBtn, text='麵類', bg='#D9D9D9', fg='black', font=fontStyle, command=lambda: self.switch_frame(Menu, '麵類'))
        buttonTmp.pack(side='right',padx=3)
        buttonTmp = tk.Button(frameBtn, text='點心', bg='#D9D9D9', fg='black', font=fontStyle, command=lambda: self.switch_frame(Menu, '點心'))
        buttonTmp.pack(side='right',padx=3)

        new_frame = Menu(self, '飯類')
        if self.menu is not None:
            self.menu.destroy()
        self.menu = new_frame
        self.menu.pack(side=TOP, fill=BOTH, padx=50, pady=20)

        textSize = 18
        fontStyle = tkFont.Font(family="Noto Sans Mono CJK TC", size=textSize, weight='bold')

        if self.frameNext is not None:
            self.frameNext.destroy()
        self.frameNext = tk.Frame(self, bg='white', height=100)
        self.frameNext.pack(side=TOP, fill=X)
        
        if self.frameCh is not None:
            self.frameCh.destroy()
        self.frameCh = tk.Frame(self.frameNext, bg='white')
        self.frameCh.pack(side=LEFT, fill=BOTH, expand=True, padx=(50,0))

        labelCurrent = tk.Label(self.frameCh, text='已選取:', font=fontStyle, bg='white')
        labelCurrent.pack(side=TOP, fill=X)

        frameList = tk.Frame(self.frameCh)
        frameList.pack(side=TOP, fill=X)

        scrollbar = tk.Scrollbar(frameList)
        scrollbar.pack(side=RIGHT, fill=Y)

        if self.listbox is not None:
            self.listbox.destroy()
        self.listbox = tk.Listbox(frameList, yscrollcommand=scrollbar.set, font=fontStyle)
        if self.meal == 'breakfast':
            FOOD = self.data.breakfast
        else:
            FOOD = self.data.lunch

        for key, value in FOOD.items():
            if value != 0:
                ss = f'{key}:{value}'
                self.listbox.insert("end",ss)
        self.listbox.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar.config(command=self.listbox.yview)
        if self.meal == 'breakfast':
            buttonNext = tk.Button(self.frameNext, text="下一步", bg='#2E75B6', fg='white', font=fontStyle, command=lambda: self.master.switch_frame(PageMeal, 'lunch'))
        else:
            buttonNext = tk.Button(self.frameNext, text="下一步", bg='#2E75B6', fg='white', font=fontStyle, command=lambda: self.master.switch_frame(PageSuggestion))
        buttonNext.pack(side=RIGHT, anchor=SE, padx=(30,30), pady=(0,30))


    def switch_frame(self, frame_class, cat):
        new_frame = frame_class(self, cat)
        if self.menu is not None:
            self.menu.destroy()
        self.menu = new_frame
        self.menu.pack(side=TOP, fill=BOTH, padx=50, pady=20)

        textSize = 18
        fontStyle = tkFont.Font(family="Noto Sans Mono CJK TC", size=textSize, weight='bold')

        if self.frameNext is not None:
            self.frameNext.destroy()
        self.frameNext = tk.Frame(self, bg='white', height=100)
        self.frameNext.pack(side=TOP, fill=X)
        
        if self.frameCh is not None:
            self.frameCh.destroy()
        self.frameCh = tk.Frame(self.frameNext, bg='white')
        self.frameCh.pack(side=LEFT, fill=BOTH, expand=True, padx=(50,0))

        labelCurrent = tk.Label(self.frameCh, text='已選取:', font=fontStyle, bg='white')
        labelCurrent.pack(side=TOP, fill=X)

        frameList = tk.Frame(self.frameCh)
        frameList.pack(side=TOP, fill=X)

        scrollbar = tk.Scrollbar(frameList)
        scrollbar.pack(side=RIGHT, fill=Y)

        if self.listbox is not None:
            self.listbox.destroy()
        self.listbox = tk.Listbox(frameList, yscrollcommand=scrollbar.set, font=fontStyle)
        for key, value in self.data.breakfast.items():
            if value != 0:
                ss = f'{key}:{value}'
                self.listbox.insert("end",ss)
        self.listbox.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar.config(command=self.listbox.yview)
        
        if self.meal == 'breakfast':
            buttonNext = tk.Button(self.frameNext, text="下一步", bg='#2E75B6', fg='white', font=fontStyle, command=lambda: self.master.switch_frame(PageMeal, 'lunch'))
        else:
            buttonNext = tk.Button(self.frameNext, text="下一步", bg='#2E75B6', fg='white', font=fontStyle, command=lambda: self.master.switch_frame(PageSuggestion))
        buttonNext.pack(side=RIGHT, anchor=SE, padx=(30,30), pady=(0,30))
        

class PageSuggestion(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.data = master.data
        self.master = master
        self.configure(bg='white')

        textSize = 18
        fontStyle = tkFont.Font(family="Noto Sans Mono CJK TC", size=textSize, weight='bold')
        
        '''
        >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>Add your code here<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
        # self.data.name str
        # self.data.height float
        # self.data.weight float
        # self.data.gender int (0->female 1->male)
        # self.data.age int
        # self.data.breakfast dict
        # self.data.lunch dict
        '''
        print(self.data.breakfast.keys())
        kcal = 0
        for key, value in self.data.breakfast.items():
            kcal += KCAL[key]*value
            print(key, value)

        ss = '你的BMI指數是： AA.A (過輕)\n'
        labelBMI = tk.Label(self, text=ss, font=fontStyle, bg='white')
        labelBMI.pack(side=TOP, anchor=NW, padx=(50,0), pady=(50,0))
        
        label = tk.Label(self, text='建議結果：', font=fontStyle, bg='white')
        label.pack(side=TOP, anchor=NW, padx=(50,0), pady=(20,0))

        print(self.data)

if __name__ == '__main__':
    database = 'data'
    data = Data(database)
    gui = GUI(data)
    gui.mainloop()

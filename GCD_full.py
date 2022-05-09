import os
import originpro as op
import pandas as pd
from loadexp import *
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit
import numpy as np
# from sklearn.datasets import make_regression
# from sklearn.linear_model import HuberRegressor, Ridge
# from sklearn import linear_model, datasets
import matplotlib.colors as mcolors
import shutil
from loadexp_0318 import folderloads

#plt.style.use('science')
year_path  = "D:\\Researcher\\JYCheon\\DATA\\Electrochemistry\\2022\\Raw"


#from IPython import get_ipython
#get_ipython().magic('reset -sf')

def supercap_func(x, a, b):
    return a*x + b

class Supercap(Dataloads):
    def __init__(self, path, file):
        Dataloads.__init__(self, path, file)
        self.name = self.name.replace("CstC_", "")
        self.df = pd.read_csv(self.file_path, sep = '\t', header = 0)
        self.df.drop(columns = 'Unnamed: 2', inplace = True)
        self.cap_result = 0
        self.appl_input = 0
        self.appl_unit = ''
        self.Is = 0
        # self.df.columns = ["time/s", '<Ewe>/V']
    
    def get_filename(self):
        return self.file
    
    def get_origin(self):
        self.origin = self.df.iloc[0, 0]
        self.df['time/s'] = self.df['time/s'].apply(lambda x: x - self.origin)
    
    def get_mpl(self, condition):
        self.condition = condition
        self.condition_path = os.path.join(self.path, self.condition)
         
    def __str__(self):
        self.label = self.name.replace("_", "-")
        return self.label
    
    def get_name(self):
        return Supercap.__str__(self)
    
    def get_condition(self, skips = 37):
        self.condition_df = pd.read_csv(self.condition_path, skiprows = skips, encoding = "utf-8") 
        self.target = self.condition_df.columns[0] 
        if self.target[:2] == 'Is':
            tmp1 = self.target.split(" ")
            tmp2 = list(set(tmp1))
            tmp2.remove("")
            tmp2.remove("Is")     
            tmp3 = sorted(tmp2)[-1]
            
            self.appl_input = float(tmp3)
    
        else:
            # Supercap.get_condition(self, skips + 1)
            return self.get_condition(skips + 1)
       

    def get_current(self):
        # self.get_condition()
        self.condition_unit = self.condition_df.iloc[0, 0][20:22] 
        self.appl_unit = self.condition_unit
        if self.condition_unit == 'mA':
            self.Is = self.appl_input/ 1000 # convert to A
            
        elif self.condition_unit == 'uA':
            self.Is = self.appl_input/1000000
    
    def get_current_condition(self):
        # self.get_condition()
        return str(self.appl_input) + ' ' + self.appl_unit
            
    def cap_plot(self):
        duration = round(float(self.get_discharge()), 2)
        applied_current = self.appl_input
        if len(applied_current) >= 4:
            applied_current = str(int(applied_current)/1000)
            Is = applied_current + 'mA'
            
        else:
            Is = applied_current + r'$\mu$A'
        try:
            label  = Supercap.__str__(self).replace("CstC-", "") + ": " + str(duration) + "s, "  + Is
        except:
            label  = Supercap.__str__(self) + ": " + str(duration) + "s, "  + Is
        plt.plot(self.df['time/s'], self.df['<Ewe>/V'],'--', color = 'gray', label = label)
        # plt.title(Supercap.__str__(self) , fontsize = 8)
        leg = plt.legend(fontsize = 5, loc = "upper left")
        for line, text in zip(leg.get_lines(), leg.get_texts()):
            text.set_color(line.get_color())
        
        
        plt.xlabel('Time (s)', fontsize = 13)
        plt.xticks(fontsize = 11)
        plt.ylabel('Voltage (V)', fontsize = 13)
        plt.yticks(fontsize = 11)

    def get_discharge(self):
        self.max = self.df['<Ewe>/V'].idxmax()
        self.discharge = self.df.loc[self.max+1 :]
        self.min = self.discharge['<Ewe>/V'].idxmin()
        self.duration =   self.df.loc[self.min]["time/s"] - self.df.loc[self.max]["time/s"]
        return self.duration
        
    
    def get_split(self):
        self.lastidx = self.discharge.shape[0]
        self.half = int((2*self.max + self.lastidx) /2)
        self.quarters = {}
        for i in range(5):
            self.quarters[i] = int(self.max + (i/8)*self.lastidx)
           
    def gethalf(self):
        self.halfX = self.df.iloc[self.max +5 : self.half, 0] 
        self.halfY = self.df.iloc[self.max +5 : self.half, 1] 
        return ( np.array(self.halfX), np.array(self.halfY) )

    def getquarter(self, qt):        
        if qt ==1:
            qt0 = int(self.max + (1/16)*self.lastidx)
            self.qtX = self.df.iloc[qt0 : self.quarters[qt], 0]
            self.qtY = self.df.iloc[qt0 : self.quarters[qt], 1]
        else:
            self.qtX = self.df.iloc[self.quarters[qt-1] : self.quarters[qt], 0]
            self.qtY = self.df.iloc[self.quarters[qt-1] : self.quarters[qt], 1]
        return ( np.array(self.qtX), np.array(self.qtY) )
    
    def get_fit(self, qt):
        # self.get_condition()
        applied_input = int(self.appl_input)
        self.popt, self.pcov = curve_fit(supercap_func, self.qtX, self.qtY)
        self.fit = supercap_func(self.qtX, *self.popt)
        self.cap = int(applied_input)/-self.popt[0] # assume applied current as uA, result: uF
        self.capacitance = round(self.cap/1000, 2) # convert to mF unit
        return self.capacitance
    
    def quarter_plot(self, qt):
        plt.plot(self.qtX, self.fit, label = "Fit quarter{0}: {1} mF".format(qt, self.capacitance))

def get_specific(name, num = -1):
    if name[:num].endswith('_'):
        condition = name[:num-1] + '.mpl'
        return condition    
    else:
        return get_specific(name, num-1)
        
def get_export(exp, path):
    output_path = path + "output\\"
    try:
        os.mkdir(output_path)
    except FileExistsError:
        pass
    with pd.ExcelWriter(output_path + "GCD_tot.xlsx") as writer:
        for i in range(len(exp)):
            
            applied_current = exp[i].appl_input
            if len(applied_current) >= 4:
                applied_current = str(int(int(applied_current)/1000))
                Is = applied_current + ' mA'
            
            else:

                Is = applied_current + ' \g(m)A'
            
            df = exp[i].df.copy()
            #if "CstC" in exp[i].name:
                #exp[i].name = exp[i].name.replace("CstC_", "")
            df.columns = ["time/s", exp[i].name +', '  +Is]
            df.to_excel(writer, startcol = 2*i, index = False)

def get_plot(exp, num, exp_dict):

    exp[num].get_origin()
    exp[num].get_mpl( exp_dict[exp[num].get_filename()] )    
    exp[num].get_condition()    
    current = exp[num].get_current()


sub_path = folderloads(year_path, None)
end_path = os.path.join(sub_path, 'Capacitance')

if os.path.exists(end_path):
    pass
    
else:
    
    folders = [_ for _ in os.listdir(sub_path) if os.path.isdir(os.path.join(sub_path, _))]
    
    if len(folders) <= 1:
        pass
        
    else:
    
    
        os.mkdir(end_path)
        
        if "Capacity" in folders:
            
            folders.remove("Capacity")
            
        
        for p in folders:
            sub = os.path.join(sub_path, p)
            target_list = os.listdir(sub)
            #file_list = [_ for _ in target_list if os.path.isfile(os.path.join(sub, _))]
            mpl_list = [_ for _ in target_list if _.endswith(".mpl")]
            txt_list = [_ for _ in target_list if _.endswith(".txt")]
            file_list = mpl_list + txt_list
            target_with_path = [os.path.join(sub, _) for _ in file_list]
            end_with_path = [os.path.join(end_path, _) for _ in file_list]
            try:
                for a, b in zip(target_with_path, end_with_path):
                    shutil.copy(a, b)
            except:
                pass        
        
    

    
file_list, path_dir, exp_path, exp_title = fileloads(year_path, '.txt')        
condition_list = [get_specific(_) for _ in file_list]
exp_dict = {}
for index, i in enumerate(file_list):
    exp_dict[i]  = condition_list[index]    
GCDs = []
CVs = []
for i in exp_dict:
    try:
        test_file = os.path.join(path_dir, exp_dict[i])
        with open(test_file, 'r') as f:  # f = open(test_file, 'r')
            lines = f.readlines()
            method = lines[2]
            if method == 'Cyclic Voltammetry\n':
                CVs.append(i)
            elif method == 'Constant Current\n':
                GCDs.append(i)
    except FileNotFoundError:
        pass        


    
    
#if len(GCDs) !=0:
    #gcd_data = build_data(path_dir, GCDs, Supercap)
    #[get_plot(gcd_data, _, exp_dict) for _ in range(len(gcd_data))]
    #get_export(gcd_data, path_dir)
    
target_path = path_dir + 'output\\'

df = pd.read_excel(target_path + 'GCD_tot.xlsx')


wks = op.find_sheet()
wks.from_df(df)

graph = op.new_graph(template = 'GCD ref3')

#plot = graph[0].add_plot(wks, colx = 0, coly = 1)
#plot2 = graph[0].add_plot(wks, colx = 2, coly = 3)


n = df.shape[1]


maxID, maxTIME = 0, 0

for i in range(0, n, 2):
    col = df.columns[i]
    lastidx = df[col].idxmax()
    
    if df[col].loc[lastidx] > maxTIME:
        maxID, maxTIME =  lastidx, df[col].loc[lastidx]
    
temp = maxTIME//50
        
        
#print(n)
for i in range(0, n, 2):
    graph[0].add_plot(wks, colx = i, coly = i+1)
    graph[0].set_xlim(0, (temp+1)*50, 50)

op.save(file = target_path + 'GCD_tot.opj')
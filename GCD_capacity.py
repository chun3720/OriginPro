import os
import originpro as op
import pandas as pd
from loadexp import *
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit
import numpy as np
import os
import shutil
from loadexp_0318 import *
year_path  = "D:\\Researcher\\JYCheon\\DATA\\Electrochemistry\\2022\\Raw"

class Supercap_Capacity(Dataloads):  
    def __init__(self, path, file):       
        Dataloads.__init__(self, path, file)
        self.df = pd.read_csv(self.file_path, sep = '\t')
        self.df.drop(columns = 'Unnamed: 2', inplace = True)
        # self.df.drop(columns = 'Unnamed: 3', inplace = True)
        # self.df.set_index('인덱스', inplace = True)
        self.null = self.df[self.df['Capacity/mA.h'] == 0].index
        self.df = self.df.drop(self.null)
        #self.df['Capacity/mA.h'] = self.df['Capacity/mA.h'].apply(lambda x: x*1000)
        self.min = self.df['<Ewe>/V'].idxmin()
        self.max = self.df['<Ewe>/V'].idxmax()
        
        #self.positive = self.df.loc[:self.max-1]
        self.positive = self.df.loc[:self.max]
        
        self.negative = self.df.loc[self.max+1 :]
        self.negative.reset_index(drop = True, inplace = True)
        
        self.data = pd.concat([self.positive, self.negative], axis = 1)
        

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
    with pd.ExcelWriter(output_path + "Capacity_tot.xlsx") as writer:
        for i in range(len(exp)):
            df = exp[i].data.copy()
            df.columns = ["charge", "voltage", "discharge", exp[i].name]
            df.to_excel(writer, startcol = 4*i, index = False)
        
        
sub_path = folderloads(year_path, None)
end_path = os.path.join(sub_path, 'Capacity')

if os.path.exists(end_path):
    pass
else:
    

    folder_list = [_ for _ in os.listdir(sub_path) if os.path.isdir(os.path.join(sub_path, _))]
    
    if len(folder_list) <= 0:
        pass
        
    else:
        os.mkdir(end_path)
        
        if "Capacitance" in folder_list:
            folder_list.remove("Capacitance")

        for p in folder_list:
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
            
            

file_list, path_dir, _, _ = fileloads(year_path, '.txt')        
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


    
    
if len(GCDs) !=0:
    gcd_data = build_data(path_dir, GCDs, Supercap_Capacity)
    get_export(gcd_data, path_dir)
    
    
target_path = path_dir + 'output\\'

df = pd.read_excel(target_path + 'Capacity_tot.xlsx')


wks = op.find_sheet()
wks.from_df(df)

graph = op.new_graph(template = 'Capacity-ref')

#plot = graph[0].add_plot(wks, colx = 0, coly = 1)
#plot2 = graph[0].add_plot(wks, colx = 2, coly = 3)


n = df.shape[1]

#print(n)
for i in range(0, n, 2):
    graph[0].add_plot(wks, colx = i, coly = i+1)
    
    
op.save(file = target_path + 'Capacity_tot.opj')
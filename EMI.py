from loadexp import *
import pandas as pd
import os
import string
import numpy as np
from matplotlib import pyplot as plt
import originpro as op

year_path = "D:\\Researcher\\JYCheon\\DATA\\EMI"

class EMI_builder(Dataloads):
    def __init__(self, path, file):
        Dataloads.__init__(self, path, file)
        self.df = pd.read_csv(self.file_path, skiprows = 8, encoding = "utf-8", sep = ' ' )
        self.df.columns = ["Frequency", "s11r", "s11i", "s21r", "s21i", "s12r", "s12i", "s22r", "s22i"]
        #convert Frequency (Hz) to GHz
        self.df["Frequency"] = self.df["Frequency"]/10**9
        
    def __str__(self):
        return self.name.replace("_", "-")
    
    def get_name(self):
        return self.name
        
        
    def get_calc(self):
        self.df["SE"] = 20*np.log10(1/np.sqrt(self.df["s21r"]**2 + self.df["s21i"]**2))
        self.df["SER"] = -10*np.log10(1-(self.df["s11r"]**2+ self.df["s11i"]**2))
        self.df["SEA"] = -10*np.log10((self.df["s21r"]**2+self.df["s21i"]**2)/(1-(self.df["s11r"]**2 + self.df["s11i"]**2)))
        
        
raw_list, path, _ , _ = fileloads(year_path, '.s2p')
exp_data = build_data(path, raw_list, EMI_builder)





for i in range(len(exp_data)):
    
    exp_data[i].get_calc()
    wks = op.new_sheet(type = 'w')
    wks.from_df(exp_data[i].df)
    wks.set_formula('A', 'A * 10^9')
    graph = op.new_graph(template = 'EMI2')
    graph[0].add_plot(wks, colx = 0, coly = 9)
    graph[0].add_plot(wks, colx = 0, coly = 10)
    graph[0].add_plot(wks, colx = 0, coly = 11)
    #graph[0].label("test").remove()
    #export_path = os.path.join(path, 'output'
    
    name = exp_data[i].name + '.opj'
    op.save(file = path + name)
    

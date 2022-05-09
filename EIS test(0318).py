import os
import originpro as op
import pandas as pd
from loadexp import *
import numpy as np
from openpyxl import load_workbook


year_path = "D:\\Researcher\\JYCheon\\DATA\\Electrochemistry\\EIS\\2022"


class EIS_builder(Dataloads):
    def __init__(self, path, file):
        Dataloads.__init__(self, path, file)
        self.df = pd.read_excel(self.file_path, sheet_name = 1, usecols = [8, 11, 12])
        
        self.outdf = self.df.copy()
        self.outdf.columns = ["Frequency", "Zreal_Ohm", "minusZim_Ohm"]
        
        self.outdf["minusZim_Ohm"] =  -self.outdf["minusZim_Ohm"]
        self.output_path = path + 'output\\'
        try:
            os.mkdir(self.output_path)    
        except FileExistsError:
            pass        
   
    
        
def EIS_export(path, exp):

    with pd.ExcelWriter(exp[-1].output_path + "total.xlsx") as writer:
        for i in range(len(exp)):
            
            df = exp[i].outdf[exp[i].outdf.columns[1:]].copy()
            df.columns = ["X", exp[i].name]
            df.to_excel(writer, startcol = 2*i, index = False)
            
raw_list, path, _, _ = fileloads(year_path, '.xlsb')
exp_data = build_data(path, raw_list, EIS_builder)

EIS_export(path, exp_data)

tot_file = os.path.join(exp_data[-1].output_path, "total.xlsx")

df = pd.read_excel(tot_file)
wks = op.find_sheet()
wks.from_df(df)
graph = op.new_graph(template = 'EIS ref')
n = df.shape[1]
maxID, maxEIS = 0, 0
for i in range(0, n, 2):
    col = df.columns[i]
    lastidx = df[col].index.to_list()[-1]
    if df[col].loc[lastidx] > maxEIS:
        maxID, maxEIS = lastidx, df[col].loc[lastidx]
    
    

#print(n)
for i in range(0, n, 2):
    graph[0].add_plot(wks, colx = i, coly = i+1)
    graph[0].set_xlim(0, maxEIS*1.1, 20)
    graph[0].set_ylim(0, maxEIS*1.1, 20)
   
    
op.save(file = exp_data[-1].output_path + 'total.opj')
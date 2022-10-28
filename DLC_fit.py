from loadexp import *
import pandas as pd
import os
import numpy as np
import originpro as op
import math

#year_path  = "D:\\Researcher\\JYCheon\\DATA\\Electrochemistry\\2022\\Raw"
py_name = "EC_DLC_from_CV_mpt.py"

path_df, path_file = get_data_folder(py_name)

year_path, template = path_df.loc[py_name]
if not template:
    path_df["op"].loc[py_name] = load_template()
    path_df.to_pickle(path_file)


raw, path, _, _ = fileloads(year_path, ".xlsx")
#exp_obj = build_data(path, raw, Supercap)

#target_path = path + 'Capacitance\\output\\'
#output_path = f'{path}\\output\\'

#xl_file = [_ for _ in os.listdir(output_path) if _.endswith('xlsx') ]

#df = pd.read_excel(f'{output_path}{xl_file[0]}', sheet_name = 1)
df = pd.read_excel(f'{path}summary.xlsx')

wks = op.find_sheet()
cols = df.columns
#wks.from_df(df[cols[:3]])
wks.from_df(df)
graph = op.new_graph(template = path_df["op"].loc[py_name])
n = df.shape[1]

maxID, maxTIME = 0, 0

#for i in range(0, n, 2):
    #col = df.columns[i]
    #lastidx = df[col].idxmax()
    #
    #if df[col].loc[lastidx] > maxTIME:
        #maxID, maxTIME =  lastidx, df[col].loc[lastidx]
    
temp = maxTIME//50

#print(n)
for i in range(0, n, 3):
    graph[0].add_plot(wks, colx = i, coly = i+1)
    graph[0].add_plot(wks, colx = i, coly = i+2)
    #graph[0].set_xlim(0, (temp+1)*50, 50)
    #graph[0].add_plot(wks, colx = i+2, coly = i+3)


#op.save(file = path + 'output\\' + 'GCD_tot.opj')
op.save(file = f'{path}DLC_tot.opj')
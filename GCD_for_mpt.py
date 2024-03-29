from loadexp import *
import pandas as pd
import os
import numpy as np
import originpro as op


# plt.style.use('science')
#year_path  = "D:\\Researcher\\JYCheon\\DATA\\Electrochemistry\\2022\\Raw"
py_name = "Supercap_GCD_mpt.py"
path_df, path_file = get_data_folder(py_name)

year_path, template = path_df.loc[py_name]
if not template:
    path_df["op"].loc[py_name] = 'GCD ref3-small'
    path_df.to_pickle(path_file)

raw, path, _, _ = fileloads(year_path, ".mpt")
#exp_obj = build_data(path, raw, Supercap)

#target_path = path + 'Capacitance\\output\\'
output_path = f'{path}\\output\\'
#df = pd.read_excel(f'{output_path}GCD_tot.xlsx')
df = pd.read_pickle(f'{output_path}GCD_tot.pkl')
wks = op.find_sheet()
wks.from_df(df)
graph = op.new_graph(template = path_df["op"].loc[py_name])
n = df.shape[1]

maxID, maxTIME = 0, 0

for i in range(0, n, 2):
    col = df.columns[i]
    lastidx = df[col].idxmax()
    
    if df[col].loc[lastidx] > maxTIME:
        maxID, maxTIME =  lastidx, df[col].loc[lastidx]
    
temp = maxTIME//50


for i in range(0, n, 2):
    graph[0].add_plot(wks, colx = i, coly = i+1)
    graph[0].set_xlim(0, (temp+1)*50, 50)


op.save(file = path + 'output\\' + 'GCD_tot.opj')
#op.save(file = f'{path}output\\GCD_tot.opj')
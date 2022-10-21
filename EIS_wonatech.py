from loadexp import *
import pandas as pd
import os
import numpy as np
import originpro as op


# plt.style.use('science')
#year_path  = "D:\\Researcher\\JYCheon\\DATA\\Electrochemistry\\EIS"


py_name = "EIS_wonatech.py"
path_df, path_file = get_data_folder(py_name)

year_path, template = path_df.loc[py_name]
if not template:
    path_df["op"].loc[py_name] = 'EIS ref'
    path_df.to_pickle(path_file)



raw, path, _, _ = fileloads(year_path, "csv")

#if "raw_split" in os.listdir(path):
    #output_path = f'{path}\\raw_split\\output\\'
    #
#else:
    #output_path = path
#exp_obj = build_data(path, raw, Supercap)

#target_path = path + 'Capacitance\\output\\'
output_path = f'{path}\\output\\'
df = pd.read_excel(f'{output_path}EIS_total.xlsx')
wks = op.find_sheet()
wks.from_df(df)
graph = op.new_graph(template = template)
n = df.shape[1]

maxID, maxTIME = 0, 0

#for i in range(0, n, 2):
    #col = df.columns[i]
    #lastidx = df[col].idxmax()
    #
    #if df[col].loc[lastidx] > maxTIME:
        #maxID, maxTIME =  lastidx, df[col].loc[lastidx]
    #
#temp = maxTIME//50

#print(n)
for i in range(0, n, 2):
    graph[0].add_plot(wks, colx = i, coly = i+1)
    #graph[0].set_xlim(0, (temp+1)*50, 50)


    
#op.save(file = output_path + 'EIS_tot.opj')
op.save(file = path + 'EIS_total.opj' )
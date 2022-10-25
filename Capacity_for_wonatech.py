from loadexp import *
import pandas as pd
import os
import numpy as np
import originpro as op


# plt.style.use('science')
#year_path = "D:\\Researcher\\JYCheon\\DATA\\Electrochemistry\\Coin cell\\2022"
py_name = "Battery_GCD_wonatech.py"
path_df, path_file = get_data_folder(py_name)

year_path, template = path_df.loc[py_name]
if not template:
    path_df["op"].loc[py_name] = 'Capacity-coin'
    path_df.to_pickle(path_file)


raw, path, _, _ = fileloads(year_path, ".pqt")
#exp_obj = build_data(path, raw, Supercap)

target_path = os.path.join(path, 'output\\')
#target = os.path.join(f'{target_path}total.xlsx')
target = os.path.join(f'{target_path}total.pkl')
#df = pd.read_excel(path +'\\split\\Capacity_tot.xlsx')
#df = pd.read_excel(target)
df = pd.read_pickle(target)

# convert to mAh/g unit

col_name = df.columns


for i in range(0, len(col_name), 2):
    col = col_name[i] 
    df[col] = df[col] * 1000


wks = op.find_sheet()
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
    #
#temp = maxTIME//50

#print(n)
for i in range(0, n, 4):
    graph[0].add_plot(wks, colx = i, coly = i+1)
    graph[0].add_plot(wks, colx = i+2, coly = i+3)
    #graph[0].set_xlim(0, (temp+1)*50, 50)

op.save(file = f'{target_path}Capacity_tot.opj')
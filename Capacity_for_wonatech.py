from loadexp import *
import pandas as pd
import os
import numpy as np
import originpro as op


# plt.style.use('science')
year_path = "D:\\Researcher\\JYCheon\\DATA\\Electrochemistry\\Coin cell\\2022"


raw, path, _, _ = fileloads(year_path, ".xlsx")
#exp_obj = build_data(path, raw, Supercap)

target_path = os.path.join(path, 'split\\output\\')
target = os.path.join(f'{target_path}total.xlsx')
#df = pd.read_excel(path +'\\split\\Capacity_tot.xlsx')
df = pd.read_excel(target)
wks = op.find_sheet()
wks.from_df(df)
graph = op.new_graph(template = 'GCD coin')
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
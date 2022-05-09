from loadexp import *
import pandas as pd
import os
import numpy as np
import originpro as op


# plt.style.use('science')
year_path = "D:\\Researcher\\JYCheon\\DATA\\Electrochemistry\\Coin cell\\2022\\"

raw, path, _, _ = fileloads(year_path, ".xlsx")
output_path = f'{path}\\output\\'
df = pd.read_excel(f'{output_path}Cycle_tot.xlsx')
wks = op.find_sheet()
wks.from_df(df)
graph = op.new_graph(template = 'Cycle tot')
n = df.shape[1]

#maxID, maxTIME = 0, 0
#
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

#op.save(file = path + 'output\\' + 'GCD_tot.opj')
op.save(file = f'{path}output\\Cycle_tot.opj')
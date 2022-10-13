from loadexp import *
import pandas as pd
import os
import numpy as np
import originpro as op


# plt.style.use('science')
year_path  = "D:\\Researcher\\JYCheon\\DATA\\Electrochemistry\\2022\\Raw"


raw, path, _, _ = fileloads(year_path, ".mpt")
#exp_obj = build_data(path, raw, Supercap)

#target_path = path + 'Capacitance\\output\\'
output_path = f'{path}\\output\\'
df = pd.read_excel(f'{output_path}Capacity_tot.xlsx')
n = df.shape[1]
check = input("convert to specific capcity?: yes(y) or no(n)")

if check.lower() == "y":
    
    cols = df.columns
    i = 3
    
    while i < n:
        
        mass = input(f"input areal density for data <{cols[i]}> (mg/cm2): ")
        area = input(f"input electrode area for data <{cols[i]}> (cm2): " )
        
        loading = float(mass) * float(area)
        
        for j in range(i-3, i, 2):
            df[cols[j]] = df[cols[j]] * 1000 / loading
        
        i += 4
        

wks = op.find_sheet()
wks.from_df(df)

template = "Capacity-specific" if check.lower() == "y" else 'Capacity-cycle'

graph = op.new_graph(template = template)


maxID, maxTIME = 0, 0

#for i in range(0, n, 2):
    #col = df.columns[i]
    #lastidx = df[col].idxmax()
    #
    #if df[col].loc[lastidx] > maxTIME:
        #maxID, maxTIME =  lastidx, df[col].loc[lastidx]
    
temp = maxTIME//50

#print(n)
for i in range(0, n, 4):
    graph[0].add_plot(wks, colx = i, coly = i+1)
    #graph[0].set_xlim(0, (temp+1)*50, 50)
    graph[0].add_plot(wks, colx = i+2, coly = i+3)


#op.save(file = path + 'output\\' + 'GCD_tot.opj')
if check.lower() == "y":
    op.save(file = f'{path}output\\Capacity_specific.opj')
else:
    op.save(file = f'{path}output\\Capacity_tot.opj')
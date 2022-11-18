from loadexp import *
import pandas as pd
import os
import numpy as np
import originpro as op
import math

# plt.style.use('science')
#year_path  = "D:\\Researcher\\JYCheon\\DATA\\Electrochemistry\\2022\\Raw"

py_name = "Supercap_GCD_mpt.py"
norm = "Capacity_norm_op"
specific = "Capacity_specific_op"

path_df, path_file = get_data_folder(py_name)

year_path, _ = path_df.loc[py_name]

if not path_df.loc[norm].op:
    print("select teplate for normal capacity")
    path_df.loc[norm].op = load_template()
    path_df.to_pickle(path_file)

if not path_df.loc[specific].op:
    print("select teplate for normal capacity")
    path_df.loc[specific].op = load_template()
    path_df.to_pickle(path_file)
    


raw, path, _, _ = fileloads(year_path, ".mpt")
#exp_obj = build_data(path, raw, Supercap)

#target_path = path + 'Capacitance\\output\\'
output_path = f'{path}\\output\\'
df = pd.read_pickle(f'{output_path}Capacity_tot.pkl')
#df = pd.read_hdf(f'{output_path}Capacity_tot.hdf5', key = "tot_df")
n = df.shape[1]
check = input("convert to specific capcity?: yes(y) or no(n)")

if check.lower() == "y":
    
    cols = df.columns
    i = 3
    
    while i < n:
        
        loading_input = input(f"input tap density and area for data <{cols[i]}> \n(ex: 4 mg/cm2 * 16 cm2 --> 4 * 16):  ")
        
        
        density, area = loading_input.split("*")
        #mass = input(f"input areal density for data <{cols[i]}> (mg/cm2): ")
        #area = input(f"input electrode area for data <{cols[i]}> (cm2): " )
        
        loading = float(density) * float(area)
        
        check2skip = input("Applying to all other measurements?: yes(y) or no(n) ")
        
        if check2skip.lower() =="y":
            
            for k in range(0, n, 2):
                df[cols[k]] = df[cols[k]] * 1000 /loading
                      
            break
        
        
        for j in range(i-3, i, 2):
            df[cols[j]] = df[cols[j]] * 1000 / loading
        
        i += 4
        

wks = op.find_sheet()
wks.from_df(df)

template = path_df.loc[specific].op if check.lower() == "y" else path_df.loc[norm].op

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
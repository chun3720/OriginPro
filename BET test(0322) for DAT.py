from loadexp import *
import pandas as pd
import os
import string
import numpy as np
import originpro as op
import pygaps as pg
import pygaps.parsing as pgp
import pprint
import pygaps.characterisation as pgc
from pygaps.graphing.calc_graphs import psd_plot
import matplotlib.pyplot as plt

year_path = "D:\\Researcher\\JYCheon\\DATA\\BET"

class N2_sorption(Dataloads):
    isotherms = []
    def __init__(self, path, file):
        Dataloads.__init__(self, path, file)
        self.iso = pgp.isotherm_from_commercial(self.file_path, "bel", "csv")
        #self.iso.convert_pressure(mode_to = 'relative')

    
    def get_BET(self):
        print('-------------------------------------------------------------------------------------------')
        print("BET analysis result for: ", self.file)
        print('-------------------------------------------------------------------------------------------')
        lastidx = self.iso.data(branch = "ads").shape[0]- 1
        self.TPV = self.iso.data(branch = "ads")["loading"].loc[lastidx]/647    
        print("Total pore volume is: {0} cm\u00b3/g".format(round(self.TPV, 2) ) )
        self.result = pgc.area_BET(self.iso, verbose=True)
        print('-------------------------------------------------------------------------------------------')
        #plt.show()
        
        self.SSA= self.result["area"]
        # self.TPV = self.iso.data(branch = "ads")["loading"].loc[lastidx]/647       
        self.ads_X = self.iso.data(branch = "ads")["pressure"]
        self.ads_Y = self.iso.data(branch = "ads")["loading"]
        self.des_X = self.iso.data(branch = "des")["pressure"]
        self.des_Y = self.iso.data(branch = "des")["loading"]
           
        N2_sorption.isotherms.append([self.ads_X, self.ads_Y, self.des_X, self.des_Y])
        
        self.df_ads = self.iso.data(branch = "ads")[["pressure", "loading"]].reset_index(drop = True)
        self.df_des = self.iso.data(branch = "des")[["pressure", "loading"]].reset_index(drop = True)
        self.output_df =  pd.concat([self.df_ads, self.df_des], axis = 1, ignore_index = True)
        self.output_df.columns = ["ads", self.name, "des", "Va/cm3(STP)g-1"]
     


def get_export(exp, path):
    output = path + 'export\\'
    
    try:
        os.mkdir(output)    
    except FileExistsError:
        pass        
    for i in range(len(exp)):
        
        df3 = pd.DataFrame({"BET surface area" : [exp[i].SSA], "Total pore volume" : [exp[i].TPV]})        
        df = pd.concat([exp[i].output_df, df3], axis = 1, ignore_index= True)
        df.columns = ["p/p0", "Va/cm3(STP)g-1", "p/p0", "Va/cm3(STP)g-1", "BET SSA (m2/g)", "Total Pore Volume (cm3/g)"]
        try:
            with pd.ExcelWriter(output + exp[i].name + '_corrected.xlsx') as writer:
                df.to_excel(writer, sheet_name = 'corrected')
        except PermissionError:
            pass
        

def get_Tot(exp, path):
    isotherm_list = exp[-1].isotherms
    n = len(exp)
    idx_list = []
    BET_list = []
    TPV_list = []
    
    for i in range(n):
        idx_list.append(exp[i].name)
        BET_list.append(exp[i].SSA)
        TPV_list.append(exp[i].TPV)
        
    d = {"BET SSA (m2/g)" : BET_list, "Total Pore Volume (cm3/g)" : TPV_list}
    df = pd.DataFrame(data = d, index = idx_list)  
    # tot_df = pd.DataFrame()
    with pd.ExcelWriter(path + 'export\\' + "Total.xlsx") as writer:
        for i in range(n):
            exp[i].output_df.to_excel(writer, startcol = 4*i, index = False)
        df.to_excel(writer, sheet_name = 'Summary')
            



def get_opj(exp, path):
    for i in range(len(exp)):
        
        wb= op.new_book()
        wks = op.find_sheet()
        exp[i].get_BET()
        wks.from_df(exp[i].output_df)
        col = exp[i].output_df.columns
        lastidx = exp[i].output_df[col[1]].idxmax()
        maxADS = exp[i].output_df[col[1]].loc[lastidx]
        graph = op.new_graph(lname = exp[i].name, template = 'BET1')
        graph[0].add_plot(wks, colx = 0, coly = 1)
        graph[0].add_plot(wks, colx = 2, coly = 3)
        graph[0].set_ylim(0, ((maxADS//100)+1 )* 100, 100)
        
        name = exp[i].name + '.opj'
        op.save(file = path + name)
        graph.destroy()
        wb.destroy()


def get_multiplot(path):
    wb = op.new_book()
    wks = op.find_sheet()
    df = pd.read_excel(path + 'export\\' + "Total.xlsx")
    n = df.shape[1]
    wks.from_df(df)
    graph2 = op.new_graph(template = 'BET2')
    #df.dropna(axis =0, inplace = True)
    
    maxID, maxADS = 0, 0
    for i in range(0, n, 4):
        col = df.columns[i+1]
        lastidx = df[col].idxmax()
        #print(lastidx)
        #print(df[col].loc[lastidx])
        if df[col].loc[lastidx] > maxADS:
            maxID, maxADS = lastidx, df[col].loc[lastidx]
        #print(df[col].loc[lastidx])

    temp = maxADS//100
    

    for i in range(0, n, 4):    
        graph2[0].add_plot(wks, colx = i, coly = i+1)
        graph2[0].add_plot(wks, colx = i+2, coly = i+3)
        graph2[0].set_ylim(0, (temp+1)*100, 100)
    #graph2[0].rescale()
    op.save(file  = path + 'export\\' + 'total.opj')
    
    
    
def get_legacy(exp, year_path, path):
    output_path = path + 'export\\'
    df = pd.read_excel(output_path + "Total.xlsx", sheet_name = "Summary", index_col = 0)
    # df2 = pd.read_excel(year_path + '\\legacy.xlsx', index_col = 0)   
    # df3 = pd.concat([df, df2], axis = 0)
    with pd.ExcelWriter(year_path + '\\legacy.xlsx', mode = 'a', engine = 'openpyxl',
                        if_sheet_exists = 'overlay') as writer:
        df.to_excel(writer,sheet_name = 'Summary', startrow = writer.sheets["Summary"].max_row, header = None)    
    print(df)
    # print(df2)
    
    
raw_list, path, _, _ = fileloads(year_path, '.csv')
exp = build_data(path, raw_list, N2_sorption)

get_opj(exp, path)
get_export(exp, path)
get_Tot(exp, path)
get_multiplot(path)
# if "legacy.xlsx exists in year_path:
get_legacy(exp, year_path, path)


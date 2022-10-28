# -*- coding: utf-8 -*-
"""
Created on Wed Mar 31 14:15:23 2021
last update : Feb 15 2022
@author: jycheon
"""

import os
import string
from dataclasses import dataclass
from pathlib import Path
import PySimpleGUI as sg
import pandas as pd
import sys
from typing import List

def path_gen(path, file_ext = None):
    print('\nCurrent path: ')
    print('-------------------------------------------------------------------------------------------')
    print(path)
    print('-------------------------------------------------------------------------------------------')
    path_folder = os.listdir(path)
    path_dict = {}
    if file_ext == None:
        for index, i in enumerate(path_folder):
            path_dict[index] = i
        for i in path_dict:
            print(str(i) + ' : '+  path_dict[i] )
        return path_dict
    elif file_ext != None:
        path_folder = [_ for _ in path_folder if _.endswith(file_ext)]
        for index, i in enumerate(path_folder):
            path_dict[index] = i
        for i in path_dict:
            print(str(i) + ' : '+  path_dict[i] )
        print('==========================================')       
        return path_dict

def get_sort(listitem, KeyFunction):
    sorted_list = sorted(listitem, key = KeyFunction)
    return sorted_list

def raw_check(path, file_ext):
        check_list = os.listdir(path)
        check_true = [_ for _ in check_list if _.endswith(file_ext)]
        if len(check_true) != 0:
            # with_path = [path + '\\' + _ for _ in check_true]    
            with_path = [os.path.join(path,_) for _ in check_true]    
            sorted_list = get_sort(with_path, os.path.getmtime)  
            # result_list = [_.split('\\')[-1] for _ in sorted_list]
            test_list = [os.path.split(_)[1] for _ in sorted_list]
            return test_list
        else:
            return check_true

def fileloads(year_path: str, file_ext: str) -> List:  
    year_dict = path_gen(year_path)
    folder_select = input("Select folder to analyze, (move to parent path: type(.):  ")
    
    if not folder_select:
        raise SystemExit("Cancelling: no folder selected")
        
    elif folder_select == ".":
        parent_path = Path(year_path).parent
        
        return fileloads(parent_path, file_ext)
    
    else:
        
        # date_path = year_path + '\\' + year_dict[int(folder_select)] + '\\'
        date_path = os.path.join(year_path, year_dict[int(folder_select)]) + '\\'
        list_check = raw_check(date_path, file_ext) 
        if len(list_check) !=0:
            list_true = list_check
            path_true = date_path
            path_gen(path_true, file_ext)
            EXP_title = year_dict[int(folder_select)].replace("_", "-")
            return (list_true, path_true, year_dict[int(folder_select)], EXP_title)  
        # else:
        return fileloads(date_path, file_ext)

#class Dataloads(object):
    #def __init__(self, path, file):
        #self.path = path
        #self.file = file
        #self.file_path = os.path.join(self.path, self.file)
        #self.name, self.ext = os.path.splitext(self.file)
        #if "CstC" in self.name:
            #self.name = self.name.replace("CstC_", "")
            
@dataclass
class Dataloads:
    path: str
    file: str
    def __post_init__(self):
        self.file_path = os.path.join(self.path, self.file)
        self.name, self.ext = os.path.splitext(self.file)
        

        
        
def build_data(path, file, builder):
    "Build class of each file and return list of builded classes"
    data = []
    for i in range((len(file))):
        try:
            data.append(builder(path, file[i]))
        except:
            print("fail to load file: ", file[i])
            pass
    return data

#from datetime import datetime
#
#print(datetime.now().isoformat(timespec = 'minutes'))

def get_data_folder(py_name):
    curr_path = Path(sys.path[0])
    path_info = "path_ref.pkl"
    path_file = curr_path.parent.joinpath(path_info)
    
    df = pd.read_pickle(path_file)
    
    return df, path_file
    

    

def load_template():
    
    init_path = r"C:\Users\user\Documents\OriginLab\User Files"
    temp_path = sg.popup_get_file('Template is missing! please select a template', initial_folder = init_path)
    temp_file = Path(temp_path)
    if not temp_path:
        sg.popup("Cancel", "No file selected")
        raise SystemExit("Canceling: no file selected")
    else:
        sg.popup(f"The template you chose was {temp_file.name}")
        
    
    return os.path.splitext(temp_file.name)[0]
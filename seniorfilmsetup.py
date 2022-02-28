#!/usr/bin/python3

import os
import pathlib
import time
import string
import subprocess
import argparse
import fnmatch
import glob
###
from pathlib import Path, PurePath



#region VARIABLES

##############################
############ VARS ############
##############################

##### Default Hou paths ######
# Linux houdini_setup_bash
# mac houdini terminal
# win houdini command line tools

hou_18_paths = {
    "linux":"/opt/hfs18.5.759/",
    "mac":"/Applications/Houdini18.5.759/",
    "windows":""
    }




# Other vars
path_list = []
env_dict = {}

# preset paths
HOME = Path.home() # gets path for HOME variable
REPO_ROOT = Path.cwd()
#print(REPO_ROOT)
dirslist = glob.glob("%s/*/" % REPO_ROOT)
#print(dirslist)

# paths to set

PROJECT_ROOT = ''
SHOTS_ROOT = ''
ASSETS_GLOBAL_ROOT = ''

PACKAGES = ''
HDA_GLOBAL = ''

# PER SHOT VARS
BLEND = ''
GEO = ''
HIP = ''
RENDER = ''
REF = ''
TEXTURE = ''

#endregion
#region SETUP
##############################
###### SET UP FOR LATER ######
##############################
#region WORK SETUP METHODS

def get_initial_paths():
    pass



#endregion
#region HELPER SETUP METHODS
###############################
####### DIRECTORY PATHS #######
###############################

def get_path(root,target):
    new_path = PurePath(root,target)
    return new_path

#print(get_path(REPO_ROOT,"Main_Project"))

def set_path():
    pass

def compare_path():
    pass

def add_var_to_dict(d,k,v):
    #k = [ i for i, a in locals().items() if a == v][0]
    #print(k)
    d[k]=v
#add_var_to_dict(env_dict,"REPO_ROOT",REPO_ROOT)
#print(env_dict)
#print([ i for i, a in locals().items() if a == REPO_ROOT][0])

# def convert_varname_tostring(var):
#     result=''
#     result = [ i for i, a in locals().items() if a == var][0]
#     return result

# def add_arr_to_dict_varname(dictionary,arr):
#     keys=[]
#     values=[]
#     for o in arr:
#         keys.append(o)
#         var_name = convert_varname_tostring(o)
#         values.append(var_name)
#     print(keys,values)

#     # for i in range(len(array)):
#     #     v = array[i]
#     #     k = convert_varname_tostring(v)
#     #     print(k)
#     #     add_var_to_dict(dictionary,k,v)

# one=23
# two=5
# three=4
# array = [one,two,three]
# test_dict={}

# add_arr_to_dict_varname(test_dict,array)

# print(test_dict)


def add_to_arr(arr,obj):
    arr.append(obj)

def check_if_path_obj(path):
    result=''
    # checks if the variable is any instance of pathlib
    if isinstance(path, pathlib.PurePath):
        print("It's pathlib!")
        result=True
        # No PurePath
        if isinstance(path, pathlib.Path):
            print("No Pure path found here")
            if isinstance(path, pathlib.WindowsPath):
                print("We're on Windows")
            elif isinstance(path, pathlib.PosixPath):
                print("We're on Linux / Mac")
        # PurePath
        else:
            print("We're a Pure path")
            result=False

# def Check_OS_Pathtype(path):
#     result=''
#     # checks if the variable is any instance of pathlib
#     if isinstance(path, pathlib.PurePath):
#         print("It's pathlib!")
#         result=True
#         # No PurePath
#         if isinstance(path, pathlib.Path):
#             print("No Pure path found here")
#             if isinstance(path, pathlib.WindowsPath):
#                 print("We're on Windows")
#             elif isinstance(path, pathlib.PosixPath):
#                 print("We're on Linux / Mac")
#         # PurePath
#         else:
#             print("We're a Pure path")
#             result=False



###############################
######## ENV VAR STUFF ########
###############################

def check_if_var_exists():
    pass

def check_value_of_env_var():
    pass

def compare_env_value():
    pass

def unset_env_var():
    pass

def set_env_var():
    pass

#endregion

#region SETUP MAIN


#endregion
#endregion
#region LOGIC

#region HELPER LOGIC METHODS

###########################
####### User Input ########
###########################

def question_pred():
    pass

###################################
####### Dir & Config Stuff ########
###################################

# directory stuff
def create_dir_list():
    pass

def create_dirs():
    pass

def project_list():
    pass

# config stuff
def create_config_dir():
    p = pathlib.Path(REPO_ROOT,".config")
    print(p)
    p.mkdir(parents=True,exist_ok=True)


create_config_dir()


def terminal_config_file():
    pass

##############################
####### Houdini Stuff ########
##############################

def get_houdini_version():
    pass

def get_houdini_hython_path():
    pass

def get_hip_file_path():
    pass

def set_hip_file_paths():
    pass

def init_houdini():
    pass

def launch_houdini():
    pass


#endregion
#region WORK LOGIC METHODS

###############################
####### User Interface ########
###############################



#endregion
#region LOGIC FINAL

#endregion
#region EXECUTE
def main():
    pass

#endregion

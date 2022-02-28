#!/usr/bin/python3

from curses import raw
from mmap import ACCESS_WRITE
import os
import time
import string
import subprocess
import argparse
import fnmatch
import glob
import sys
import tkinter
from xml.etree.ElementInclude import include
import pip
from tkinter import Tk, filedialog
from itertools import chain, repeat
from pathlib import Path
### other file

#### check for module

# def import_or_install(package):
#     try:
#         __import__(package)
#     except ImportError:
#         pip.main(['install', package])  

# import_or_install(tkinter)


### choose repo ####
# root = Tk() # pointing to root
# root.withdraw() # hides small window

# root.attributes('-topmost',True) #opened windows will be active

# open_file = filedialog.askdirectory() #returns opened path as string

# print(open_file)

#### Helper Methods ####

def user_question(prompt):
    answers = {"y","n"}
    prompts = chain([prompt], repeat("Please answer with y/n: "))
    replies = map(input, prompts)
    valid_response = next(filter(answers.__contains__, replies))
    #print(valid_response)
    return valid_response


def question_predicate(answer):
    #print(valid_response)
    if answer == "y":
        value = True
    elif answer == "n":
        value = False
    return value

def answer_pred(prompt):
    answer = user_question(prompt)
    value = question_predicate(answer)
    return value

#test = question_predicate(user_question("test"))
#print(test)


#### Include Repo ####
def choose_repo_path():
    path = input("Enter or paste path to repo: ")
    #print(path)
    pred = question_predicate(user_question("Is this path correct? " + path + ": y/n "))

    


def Incude_repo():
    include_repo_answer = user_question("do you want to include a tool repo? ")
    pred = question_predicate(include_repo_answer)
    
    if pred:
        #repo_path = os.path(choose_repo_path())
        #script_path = os.path.join(repo_path,"reposetup.py")
        #os.system("python /home/ben/Houdini_Stuff/Houdini-HDA-Collection/repoSetup.py")
        output = subprocess("python /home/ben/Houdini_Stuff/Houdini-HDA-Collection/repoSetup.py",shell=True)
        print(output)
        #print(script_path)
        #subprocess(script_path,shell=True)
    else:
        pass

def Write_To_File():
    File_Object = open(r"tools.env",ACCESS_WRITE)


def Convert_Path_To_Win():
    pass

Incude_repo()


##### Next #####


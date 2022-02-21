#!/usr/bin/python3

import os
import time
import string
import subprocess
import argparse
import fnmatch
import glob
import sys


# find required 
required = {'GitPython'}
installed = {pkg.key for pkg in pkg_resources.working_set}
missing = required - installed

if missing:
    python = sys.executable
    subprocess.check_call([python, '-m', 'pip', 'install', *missing], stdout=subprocess.DEVNULL)


### Check Repo


### find paths



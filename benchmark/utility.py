import os
from pathlib import Path
import shutil

import config
import openml

def prepare_experiment_directory(path):
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path)        

def prepare_cache_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)

def prepare_OpenML():
    openml.config.apikey = config.OPENML_APIKEY
    openml.config.cache_directory = os.path.expanduser('~/.openml/cache')

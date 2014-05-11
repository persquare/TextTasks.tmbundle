#!/usr/bin/env python
# encoding: utf-8

# This file is part of the TextTasks bundle for TextMate2.
# It contains helper functions for dealing with todo-lists.

import sys
import os
import shutil
import imp

from os import listdir
from os.path import isfile, join

## 
# Project file handling
#     
def is_project_file(path, filename):
    global options
    if isfile(join(path, filename)):
        (name, ext) = os.path.splitext(filename)
        if ext in options.PROJEXTS:
            return True
    return False
        
def list_projects():
    global options
    files = [ f for f in listdir(options.PROJPATH) if is_project_file(options.PROJPATH, f) ]
    projects = [os.path.splitext(file)[0] for file in files]
    return projects
    
def file_for_project(proj):
    global options
    # find <proj>.<ext1|ext2|...|ext3>
    for file in listdir(options.PROJPATH):
        (name, ext) = os.path.splitext(file)
        if name == proj and ext in options.PROJEXTS:
            return os.path.join(options.PROJPATH, file)
    return None
    
def add_lines_to_project(lines, proj):
    
    filename = file_for_project(proj)
    if not filename:
        return False
        
    f = open(filename,'r')
    temp = f.read()
    f.close()

    f = open(filename, 'w')
    f.write(lines)
    f.write('\n')
    f.write(temp)
    f.close()
    
    return True
    

## 
# Options
#     
def _options_file():
    # IF $TM_TEXTTASKS_OPTIONS_FILE is set:
    #   options_file = $TM_TEXTTASKS_OPTIONS_FILE
    # ELSE /* not set */
    #   options_file = ~/.texttasks_options
    # END
    # IF NOT (file $options_file exists):
    #   COPY defaults file to location $options_file
    # END
    # OPEN/READ $options_file
    
    options_file = os.environ.get('TM_TEXTTASKS_OPTIONS_FILE', '~/.texttasks_options')
    options_file = os.path.expanduser(options_file)
    if not os.path.isfile(options_file):
        default_file = os.environ['TM_BUNDLE_SUPPORT'] + '/tt_config.py'
        shutil.copy (default_file, options_file)
    
    return options_file

def update_options():
    global options
    options_file = _options_file()
    options = imp.load_source('options', options_file)
    
    
def open_options_file():
    options_file = _options_file()
    os.system('open -a TextMate %s' % options_file)

update_options()


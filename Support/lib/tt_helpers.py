#!/usr/bin/env python
# encoding: utf-8

# This file is part of the TextTasks bundle for TextMate2.
# It contains helper functions for dealing with todo-lists.

import sys
import os
import shutil
import imp

def _prepend_lines_to_file(lines, filename):
    with open(filename,'r') as original: 
        data = original.read()
    with open(filename, 'w') as modified:
        for line in lines:
            modified.write(line + '\n')
        modified.write(data)
        modified.flush()    

## 
# Options
#     
def _options_file():
    # Find location of options file    
    options_file = os.environ.get('TM_TEXTTASKS_OPTIONS_FILE', '~/.texttasks_options')
    options_file = os.path.expanduser(options_file)  
    # If no file exists at that location, copy over the default options file
    if not os.path.isfile(options_file):
        default_file = os.environ['TM_BUNDLE_SUPPORT'] + '/tt_config.py'
        shutil.copy (default_file, options_file)
    return options_file

def read_options():
    return imp.load_source('options', _options_file())
    
def open_options_file():
    os.system('open -a TextMate %s' % _options_file())
    
## 
# Project file handling
#     
class Projects(object):
    """Encapsulate TextTasks projects"""
    def __init__(self):
        super(Projects, self).__init__()
        options = read_options()
        projects = {}
        tt_dirs = [os.path.expandvars(p) for p in options.PROJECT_DIRS]
        if os.environ['TM_DIRECTORY'] not in tt_dirs:
            tt_dirs.insert(0, os.environ['TM_DIRECTORY'])
        for path in [p for p in tt_dirs if os.path.isdir(p)]:
            for filename in os.listdir(path):
                (name, ext) = os.path.splitext(filename)
                if ext in options.FILE_EXTS:
                    projects[name] = os.path.join(path, filename)
        self.projects = projects
        
    def is_project_file(self, file):
        return (os.path.expandvars(file) in self.projects.values())
        
    def list_projects(self):
        return self.projects.keys()
    
    def file_for_project(self, proj):
        return self.projects.get(proj, None)
    
    def add_tasks_to_project(self, tasks, proj):          
        filename = self.projects.get(proj, None)
        if not filename:
            return False
        _prepend_lines_to_file(tasks, filename)
        return True
    
if __name__ == '__main__':
    p = Projects()
    print p.is_project_file('/foo.todo')
    print p.is_project_file('${HOME}/Dropbox/Lists/foo.todo')
    print
    print "Projects:"
    for l in p.list_projects():
        print '   ' + l
    print
    print p.file_for_project('test')
    print p.file_for_project('test2')
    print
    print p.add_tasks_to_project(['- added task'], 'foo')
    print p.add_tasks_to_project(['- added task'], 'baz')
    print 
    print _options_file()
    print 
    print type(read_options())
    


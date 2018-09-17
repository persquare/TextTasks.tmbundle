#!/usr/bin/env python
# encoding: utf-8

# This file is part of the TextTasks bundle for TextMate2.
# It contains helper functions for dealing with todo-lists.

import sys
import os
import shutil
import imp
import re

def _prepend_lines_to_file(lines, filename):
    with open(filename,'r') as original:
        data = original.read()
    with open(filename, 'w') as modified:
        for line in lines:
            lineln = line + '\n'
            modified.write(lineln.encode('utf-8'))
        modified.write(data)
        modified.flush()


##
# Project file handling
#
class Projects(object):
    """Encapsulate TextTasks projects"""
    def __init__(self):
        super(Projects, self).__init__()
        projects = {}
        PROJECT_DIRS = os.environ.get('TT_PROJECT_DIRS', 'PWD').split(':')
        FILE_EXTS = os.environ.get('TT_FILE_EXTS', '.todo').split(',')
        EXCLUDE = [x.strip() for x in os.environ.get('TT_EXCLUDE', '').split(',') if x != '']
        tt_dirs = [os.path.expandvars(p) for p in PROJECT_DIRS]
        current_dir = os.environ.get('TM_DIRECTORY')
        if current_dir and current_dir not in tt_dirs:
            tt_dirs.insert(0, current_dir)
        for path in [p for p in tt_dirs if os.path.isdir(p)]:
            for filename in os.listdir(path):
                (name, ext) = os.path.splitext(filename)
                if name in EXCLUDE:
                    continue
                if ext in FILE_EXTS:
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

    def scan_project(self, project, regex):
        """
        Scan the project file using the regex,
        return list of dicts for each line that match.
        The dicts contain 'task', 'project', 'file', 'line' keys
        """
        # cre = re.compile(regex)
        file = self.file_for_project(project)
        if not file:
            return
        line = 0
        result = []
        with open(file) as f:
            for task in f:
                line +=1
                match = re.match(regex, task)
                if match:
                    result.append({'project':project, 'task':task.strip(), 'file':file, 'line':line, 'match':match})
        return result

    def scan_all_projects(self, regex):
        result = []
        for project in self.projects:
            result += self.scan_project(project, regex)
        return result

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



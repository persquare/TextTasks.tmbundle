# This file is part of the TextTasks module.
# It contains helper functions for dealing with todo-lists.

import os

class TextTasks(object):

    """Encapsulate TextTasks projects"""
    def __init__(self, project_dirs, file_exts):
        super(TextTasks, self).__init__()
        self._projects = {}
        tt_dirs = [os.path.expandvars(p) for p in project_dirs]
        for path in [p for p in tt_dirs if os.path.isdir(p)]:
            for filename in os.listdir(path):
                (name, ext) = os.path.splitext(filename)
                if ext in file_exts:
                    self._projects[name] = os.path.join(path, filename)

    def __str__(self):
        projs = (f"  {name} : {path}" for name, path in self._projects.items())
        return "\n".join(projs)

    @property
    def projects(self):
        return list(self._projects.keys())

    def file_for_project(self, proj):
        return self._projects.get(proj, None)

    def _project_lines(self, project, scanner):
        file = self.file_for_project(project)
        context = {
            "project": project,
            "file": file,
            "line": 0,
        }
        with open(file, encoding='utf8') as f:
            for task in f:
                context['line'] +=1
                matching = scanner(task, context)
                if not matching:
                    continue
                yield matching

    def scan_project(self, project, scanner):
        """
        Scan the project file using the scanner,
        return list of tasks that match.
        """
        return [t for t in self._project_lines(project, scanner)]


    def scan_projects(self, projects, scanner):
        result = []
        for project in projects:
            result += self.scan_project(project, scanner)
        return result

    def scan(self, scanner):
        return self.scan_projects(self.projects, scanner)


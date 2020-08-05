from .scanner import full_scanner
from .task import Status, Task
from .project import Project

def _project_lines(context, scanner):
    with open(context['file'], encoding='utf8') as f:
        for raw_task in f:
            context['line'] +=1
            matching = scanner(raw_task, context)
            if not matching:
                continue
            yield matching


class Parser(object):
    """docstring for Parser"""
    def __init__(self, filename):
        super().__init__()
        self.ctx = {
            "project": 'dummy',
            "file": filename,
            "line": 0,
        }
        proj = Project(self.ctx)
        proj.indent = -1
        self.stack = [proj]
        self.indent = 0

    def _push(self, item):
        self.stack.append(item)

    def _pop(self):
        return self.stack.pop()

    def _add(self, item):
        self.stack[-1].subtasks.append(item)

    def _peek(self):
        return self.stack[-1]

    def _unroll(self, indent):
        while self._peek().indent >= indent:
            self._pop()

    def _unroll_to_heading(self):
        while self._peek().status not in (Status.HEADING, Status.PROJECT):
            self._pop()

    def _reset(self):
        self.stack = self.stack[:1]
        self.indent = 0

    def parse(self):
        for t in _project_lines(self.ctx, Task):
            if t.status is Status.HEADING:
                self._reset()
                self._add(t)
                self._push(t)
            elif t.status in (Status.COMMENT, Status.BLANK):
                self._add(t)
            elif t.status in (Status.TODO, Status.DONE, Status.CANCELLED):
                if t.indent == 0:
                    self._unroll_to_heading()
                elif t.indent < self.indent:
                    self._unroll(t.indent)
                elif t.indent == self.indent:
                    self._pop()
                self._add(t)
                self._push(t)
                self.indent = t.indent
            else:
                raise Exception(str(t))
        return self.stack[0]

def parse(filename):
    p = Parser(filename)
    return p.parse()


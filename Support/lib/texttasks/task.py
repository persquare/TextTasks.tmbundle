import re
from enum import Enum

class Status(Enum):
    BLANK = 0
    TODO = 1
    DONE = 2
    CANCELLED = 3
    COMMENT = 4
    HEADING = 5
    PROJECT = 6
    ERROR = 7


    @classmethod
    def from_marker(cls, marker):
        return {
                '+':cls.DONE,
                '-':cls.TODO,
                'x':cls.CANCELLED
            }[marker]

    def __str__(self):
        return ['-', '+', 'x'][self.value - 1] if self.value in [1,2,3] else self.name

# Regexes
RE_HEADING = r'(\s*)(.+?):\s*$'
RE_COMMENT = r'(\s*)(.+?)$'
RE_TASK = r'(\s*)([x|\+|-])\s+(.*)'
RE_TAGS = r"@([_\-a-zA-Z0-9]+)(?:\((.*?)\))?"
RE_ISTASK = r'^(\s*)([-|x|\+])\s+'


class Task(object):
    """docstring for Task"""
    def __init__(self, raw, context):
        super().__init__()
        self.project = context['project']
        self.file = context['file']
        self.line = context['line']
        self.indent = 0
        self.status = Status.BLANK
        self.description = ""
        self.tags = []
        self.subtasks = []
        self.parse(raw)

    def __str__(self):
        if not self.status:
            return ""
        if self.status in [Status.TODO, Status.DONE, Status.CANCELLED]:
            tags = " ".join(f"@{t['name']}" + (f"({t['value']})" if t['value'] is not None else "") for t in self.tags)
            return f"{' '*self.indent}{self.status} {self.description} {tags}".rstrip()
        retval = f"{' '*self.indent}{self.description}"
        if self.status is Status.HEADING:
            retval += ":"
        return retval

    def parse(self, raw):
        def _get_tags(raw):
            matches = re.finditer(RE_TAGS, raw)
            return [dict(zip(('name', 'value'), match.group(1,2))) for match in matches]
        def _get_task(raw):
            match = re.match(RE_TASK, raw)
            return len(match.group(1)), match.group(2), match.group(3).strip()
        # Blank?
        if raw.strip() == "":
            return
        # Task?
        if re.match(RE_ISTASK, raw):
            task_text, sep, tag_text = raw.partition('@')
            self.indent, marker, self.description = _get_task(task_text)
            self.tags = _get_tags(sep + tag_text)
            self.status = Status.from_marker(marker)
            return
        # Heading?
        match = re.match(RE_HEADING, raw)
        if match:
            self.status = Status.HEADING
            self.indent = len(match.group(1))
            self.description = match.group(2).strip()
            return
        # Comment?
        match = re.match(RE_COMMENT, raw)
        if match:
            self.status = Status.COMMENT
            self.indent = len(match.group(1))
            self.description = match.group(2).strip()
        else:
            # => syntax error
            self.status = Status.ERROR
            self.description = f"Error -> {raw}"

class Project(Task):
    """docstring for Project"""
    def __init__(self, context):
        super().__init__("", context)
        self.line = 0
        self.status = Status.PROJECT

    def __str__(self):
        return f"Project:'{self.project}' [{self.file}]"

    def parse(self, raw):
        pass

if __name__ == '__main__':
    s = Status.DONE
    print(s)
    print(repr(s))
    s = Status.from_marker('-')
    print(s)
    print(repr(s))

    ctx = {'project': 'foo', 'file': 'foo.todo', 'line':1}

    tests = [
        '    - do this @mit',
        '+ done',
        'x cancelled',
        'hello comment',
        '  heading:',
        '- task',
        'is this a comment: @delegated(Per)',
        '     ',
    ]
    for raw in tests:
        t = Task(raw, ctx)
        print(f"<{t}>")
        print(f"<{raw}>")
        try:
            assert(str(t)==raw.strip())
        except AssertionError as err:
            print("Error:", raw)
            print("indent", t.indent)
            print("status", t.status)
            print("description", t.description)
            print("tags", t.tags)

    p = Project(ctx)
    print(p)
    for raw in tests:
        t = Task(raw, ctx)
        p.subtasks.append(t)





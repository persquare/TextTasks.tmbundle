import re
from collections import namedtuple

def _get_tags(raw):
    RE_TAG = r"@([_\-a-zA-Z0-9]+)(?:\((.*?)\))?"
    matches = re.finditer(RE_TAG, raw)
    return [dict(zip(('name', 'value'), match.group(1,2))) for match in matches]

def _get_task(raw):
    RE_TASK = r'(\s*)([x|\+|-])\s+(.*)'
    match = re.match(RE_TASK, raw)
    return len(match.group(1)), match.group(2), match.group(3).strip()

def _task(raw):
    task_text, sep, tag_text = raw.partition('@')
    indent, status, task = _get_task(task_text)
    tags = _get_tags(sep + tag_text)
    task_data = dict(zip(("indent", "status", "description", "tags"), (indent, status, task, tags)))
    return task_data

def make_task(raw, context):
    task_data = _task(raw)
    return Task(**task_data, **context)


class Task(namedtuple('Task', "project file line indent status description tags")):
    def __str__(self):
        tags = " ".join(f"@{t['name']}" + (f"({t['value']})" if t['value'] is not None else "") for t in self.tags)
        return f"{' '*self.indent}{self.status} {self.description} {tags}"


if __name__ == '__main__':
    t = make_task("  - hello @mit @due(2020-06-30) @ fo ba(hello)", {'project':'project', 'file':'file', 'line':2})
    print(t)
    print(repr(t))







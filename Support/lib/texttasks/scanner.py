import re

from .task import Task


TAGGED_TASK_TEMPLATE = r"^(\s*)-\s+(.+?)\s(?:\s*@.+?\s)*?@{}(?:\((.*?)\)\s*)?(?:\s*@.+?)*\s*$"

def tag_scanner(tag, predicate=None):

    regex = TAGGED_TASK_TEMPLATE.format(tag)

    def scanner(task_text, context):
        match = re.match(regex, task_text)
        if not match:
            return
        task = Task(task_text, context)
        if predicate is None:
            return task
        operands = [t['value'] for t in task.tags if t['name'] == tag and t['value']]
        if not operands:
            return task
        if any(map(predicate, operands)):
            return task
        return None

    return scanner

def full_scanner():
    return Task






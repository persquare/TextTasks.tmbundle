from .task import Task, Status

class Project(Task):
    """docstring for Project"""
    def __init__(self, context):
        super().__init__("", context)
        self.line = 0
        self.status = Status.PROJECT

    def _format(self, task):
        if task.status is not Status.PROJECT:
            yield str(task)
        for t in task.subtasks:
            yield from self._format(t)

    def __str__(self):
        lines = [line for line in self._format(self)]
        return "\n".join(lines)

    def parse(self, raw):
        pass

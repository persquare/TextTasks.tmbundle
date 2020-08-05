import datetime

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

    def _task_complete(self, task):

        def _recurse_task(task):
            if task.status is Status.TODO:
                raise StopIteration
            for t in task.subtasks:
                _recurse_task(t)

        try:
            _recurse_task(task)
        except StopIteration:
            return False
        return True

    def _archive_tasklist(self, scanlist):
        archived = []
        for t in list(scanlist):
            if t.status in (Status.DONE, Status.CANCELLED):
                if self._task_complete(t):
                    scanlist.remove(t)
                    archived.append(t)
        return archived

    def archive(self):
        """
        Traverse project and move completed tasks to 'Archived' section

        Tasks are complete ONLY when neither it nor any of its subtasks (recursively) have TODO status.
        Archive section created if necessary.
        """
        # Special care should be taken to handle top-level tasks (i.e. without heading)
        archived = []
        scanlist = self.subtasks
        archive_heading = None
        for t in list(scanlist):
            if t.status is Status.HEADING and t.description == "Archive":
                archive_heading = t
                continue
            if t.status is Status.HEADING:
                archived.extend(self._archive_tasklist(t.subtasks))
            elif t.status in (Status.DONE, Status.CANCELLED):
                if self._task_complete(t):
                    scanlist.remove(t)
                    archived.append(t)

        if not archived:
            return
        if not archive_heading:
            raise Exception("FIXME: Missing Archive heading")
        archive_heading.subtasks[:0] = archived
        now = datetime.datetime.now()
        now_str = now.strftime("%Y-%m-%d %H:%M:%S")
        archive_heading.subtasks[:0] = [Task(f"---- {now_str} ----")]




    def parse(self, raw):
        pass

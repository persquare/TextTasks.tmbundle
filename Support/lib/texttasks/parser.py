from .scanner import full_scanner
from .task import Status, Task, Project

def _project_lines(context, scanner):
    with open(context['file'], encoding='utf8') as f:
        for raw_task in f:
            context['line'] +=1
            matching = scanner(raw_task, context)
            if not matching:
                continue
            yield matching


def parse(filename):
    ctx = {
        "project": 'dummy',
        "file": filename,
        "line": 0,
    }

    proj = Project(ctx)
    proj.indent = -1
    stack = [proj]
    indent = 0

    for t in _project_lines(ctx, Task):
        # Nothing special to do for COMMENT, BLANK, or task with same indent
        # FIXME: COMMENT should be subtask of latest task or heading
        # FIXME: Headings should be appended to TOS
        if t.status is Status.ERROR:
            raise Exception(str(t))
        if t.status is Status.HEADING:
            # Reset tree
            stack = [proj]
            indent = 0
            stack[-1].subtasks.append(t)
            stack.append(t)
            continue
        if t.status in [Status.TODO, Status.DONE, Status.CANCELLED] \
             and t.indent != indent:
            # Now indentation becomes important...
            # 1. increase
            if t.indent > indent:
                # move last subtask from parent task to TOS
                grandparent = stack[-1]
                if grandparent.subtasks:
                    parent = grandparent.subtasks[-1]
                    stack.append(parent)
                indent = t.indent
            # 2. decrease
            else: # t.indent < indent
                # unroll stack until indent < t.indent
                # FIXME: Don't unroll past heading
                indent = t.indent
                while stack[-1].indent >= indent and stack[-1].status is not Status.HEADING:
                    stack.pop()
        # Append task at the appropriate level
        stack[-1].subtasks.append(t)

    return proj

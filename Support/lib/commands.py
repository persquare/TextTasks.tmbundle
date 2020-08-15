import os
import sys
import re
from datetime import date, timedelta

try:
    helper = os.path.join(os.environ['TM_PYTHON_HELPERS_BUNDLE_SUPPORT'], 'lib')
    if helper not in sys.path:
        sys.path[:0] = [helper]
except:
    errmsg = """
    The PythonHelpers bundle required, see<br/>
    <a href=https://github.com/persquare/PythonHelpers.tmbundle>
    github.com/persquare/PythonHelpers.tmbundle
    </a>
    """
    sys.stderr.write(errmsg)
    sys.exit(205)


from TextMate import exit_codes as exit
from TextMate import dialog
from TextMate import webpreview as wp
from TextMate import help_gen

import texttasks

def open_project():
    conf = texttasks.config()
    projects = texttasks.TextTasks(conf.project_dirs, conf.file_exts)
    project_list = projects.projects

    r = dialog.present_menu(project_list)
    if r is None:
        exit.show_tool_tip('No selection made')
    f = projects.file_for_project(project_list[r])
    if f:
        # FIXME: Make opening files a command in Python3's TextMate module,
        #        and drop os.system in favour of subprocess
        os.system('open -a TextMate %s' % f)
        exit.discard()
    else:
        exit.show_tool_tip('Project not found')


def toggle_status():
    selection = os.environ.get('TM_SELECTED_TEXT', None)
    if selection:
        # If there is a selection I can't get access to the line?! Bail.
        exit.show_tool_tip('Selection blocks command.')
    line = os.environ.get('TM_CURRENT_LINE', None)
    line = line.rstrip('\r\n ')


    # Should not match heading
    if line.endswith(':'):
        exit.discard()

    # m = re.match(r'^(\s*)(- |\+ |x )?(.*)$', line)
    m = re.match(r'^(\s*)((?:[-\+x] )?)(.*)$', line)
    if not m:
        # Not a task => leave line as-is
        exit.show_tool_tip('Not a task: <%s>' % line)

    indent = m.group(1)
    task = m.group(3)
    marker = m.group(2).rstrip()

    if not marker:
        # Not a task => leave line as-is
        exit.discard()


    # Three cases for marker: '-', '+', 'x'
    # Cycle though them: '-' -> '+' -> 'x' -> '-' -> ...
    cycle = {'-':'+ ', '+':'x ', 'x':'- '}
    marker = cycle[marker]

    sys.stdout.write('%s%s%s' % (indent, marker, task))

def archive_completed():
    try:
        filepath = os.environ['TM_FILEPATH']
    except:
        exit.show_tool_tip(f"Failed to parse file '{os.environ.get('TM_DISPLAYNAME', '???')}'")
    proj = texttasks.parse(filepath)
    proj.archive()
    return str(proj)

def select_mit():
    conf = texttasks.config()
    projects = texttasks.TextTasks(conf.project_dirs, conf.file_exts)

    scanner = texttasks.tag_scanner('mit')
    mit_list = projects.scan(scanner)
    menuitems = ["{}: {}".format(x.project, x.description) for x in mit_list]
    choice = dialog.present_menu(menuitems)
    if choice is not None:
        task = mit_list[choice]
        cmd = "{} -l{} {}".format(os.environ['TM_MATE'], task.line, task.file)
        os.system(cmd)

def select_due():
    conf = texttasks.config()
    projects = texttasks.TextTasks(conf.project_dirs, conf.file_exts)

    lookahead = int(os.environ.get('TT_DUE_LOOKAHEAD', 14))
    then = date.today() + timedelta(days=lookahead)
    predicate = texttasks.date_predicate("<=", then.strftime("%Y-%m-%d"))
    scanner = texttasks.tag_scanner('due', predicate)
    due_list = projects.scan(scanner)
    menuitems = ["{}: {}".format(x.project, x.description) for x in due_list]
    choice = dialog.present_menu(menuitems)
    if choice is not None:
        task = due_list[choice]
        cmd = "{} -l{} {}".format(os.environ['TM_MATE'], task.line, task.file)
        os.system(cmd)

def html_help(intro='', body=''):
    parts = [
        wp.html_header('TextTasks Help', 'TextTasks'),
        help_gen.help_for_bundle(intro, body),
        wp.html_footer()
    ]
    return "\n".join(parts)


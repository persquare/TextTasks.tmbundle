import os
import sys
import re
import urllib
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
import applewrap

def augment_return_behaviour():
    """
    Augment return key behaviour depending on the caret position. There are five cases:

    1. in leading whitespace before task => insert new task before line
    2. at end of task => insert new task on new line
    3. inside task => split task at caret and insert new task on new line
    4. at end after empty task => clear empty task and align caret with leading space
    5. outside a task behave as usual unless if after a heading (2) is applied

    Returns a 'snippet' to be inserted.

    FIXME: The implementation uses a mix of return snippets and 'exit' operations.

    """

    if os.environ.get('TM_SELECTED_TEXT', None):
        # If there is a selection I can't get access to the line?! Bail.
        exit.discard()

    line = os.environ.get('TM_CURRENT_LINE')
    line = line.rstrip('\r\n ')
    col = int(os.environ.get('TM_LINE_INDEX'))

    # The zero-or-one match '- ?' in the regex below
    # is needed since ' ' are stripped off from the end of line above,
    # if there was no task, the ' ' after '-' is also removed.
    match = re.match(r'^(\s*)[-+x] ?(.*)$', line)

    if not match:
        match = re.match(r'^(.+:)\s*$', line)
        if match and col >= len(match.group(1)):
            return '\n- ${0}'
        else:
            # Not a heading => just insert newline
            return '\n'
    else:
        # exit.show_tool_tip('<%s>\n<%s>\n<%s>' % (match.group(0), match.group(1), match.group(2)))
        # Four cases:
        # 1) in leading whitespace => insert new task before
        # 2) at end => insert new task after
        # 3) inside task => split at cursor with new task after
        # 4) at end after empty task => clear empty task and align with leading space

        indent = match.group(1)
        task = match.group(2)
        indent_level = len(indent)

        # Case (4)
        if not task and col >= indent_level:
            exit.replace_text(indent)
        # Case (1)
        if col <= indent_level:
            return '%s- ${0}\n' % indent[col:]
        # Case (2) & (3)
        if col > indent_level:
            return '\n- ${0}'



def open_project():
    """
    Present a menu of projects, and open the selected one in TM

    FIXME: Make opening files a command in Python3's TextMate module,
           and drop os.system in favour of subprocess
    """

    conf = texttasks.config()
    projects = texttasks.TextTasks(conf.project_dirs, conf.file_exts)
    project_list = projects.projects

    r = dialog.present_menu(project_list)
    if r is None:
        exit.show_tool_tip('No selection made')
    f = projects.file_for_project(project_list[r])
    if f:
        os.system('open -a TextMate %s' % f)
        exit.discard()
    else:
        exit.show_tool_tip('Project not found')


def toggle_status():
    """
    Toggle task status

    FIXME: Return string instead of writing it out
    FIXME: Operate on Task objects instead of using regexes on text
    """

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
    """Return a modified document as a string"""

    try:
        filepath = os.environ['TM_FILEPATH']
    except:
        exit.show_tool_tip(f"Failed to parse file '{os.environ.get('TM_DISPLAYNAME', '???')}'")
    proj = texttasks.parse(filepath)
    proj.archive()
    return str(proj)

def select_mit():
    """
    Present a menu of MIT's, and go to the selected one in TM

    FIXME: Make opening files a command in Python3's TextMate module,
           and drop os.system in favour of subprocess
    """

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
    """
    Present a menu of due tasks, and go to the selected one in TM

    FIXME: Make opening files a command in Python3's TextMate module,
           and drop os.system in favour of subprocess
    """

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
    """Return help for the bundle in HTML format"""
    parts = [
        wp.html_header('TextTasks Help', 'TextTasks'),
        help_gen.help_for_bundle(intro, body),
        wp.html_footer()
    ]
    return "\n".join(parts)

def html_overview():
    """Return overview of clickable MIT's, due tasks, delegated tasks, and flagged email in HTML format"""

    conf = texttasks.config()

    def format_output(task):
        FMT = u'<p>{t.project} : <a href="{url}">{t.description}</a>{note}</p>'
        TXMT_URL = u'txmt://open?url=file://{t.file}&line={t.line}&column={col}'
        url = TXMT_URL.format(col=1, t=task)
        notes = [tag['value'] for tag in task.tags if tag['name'] in ('delegated', 'due') and tag['value']]
        annotation = " ({})".format(", ".join(notes)) if notes else ""
        return FMT.format(url=url, t=task, note=annotation)

    # FIXME: Copy/Drag-n-drop with appropriate client
    def format_flagged_email(flagged):
        """flagged_ is a tuple with (from, subject, message_id)"""
        sender, task, msg_id = flagged
        msg_id = urllib.parse.quote(msg_id)
        FMT = u'<p>{} : <a href="#outlook://{}" onclick="{}">{}</a></p>'
        MAIL_OPEN = u"open_mail('{}', '{}')"
        onclick_handler = MAIL_OPEN.format(conf.mail_client, str(msg_id))
        return FMT.format(sender, str(msg_id), onclick_handler, task)

    def sort_due_list(due_list):
        return due_list


    projects = texttasks.TextTasks(conf.project_dirs, conf.file_exts)

    scanner = texttasks.tag_scanner('mit')
    mit_list = projects.scan(scanner)

    lookahead = int(os.environ.get('TT_DUE_LOOKAHEAD', 14))
    then = date.today() + timedelta(days=lookahead)
    predicate = texttasks.date_predicate("<=", then.strftime("%Y-%m-%d"))
    scanner = texttasks.tag_scanner('due', predicate)
    due_list = projects.scan(scanner)

    scanner = texttasks.tag_scanner('delegated')
    delegated_list = projects.scan(scanner)

    # Remove mits from due list
    due_list = [due for due in due_list if due not in mit_list]
    # Remove delegated from mit and due lists
    due_list = [due for due in due_list if due not in delegated_list]
    # FIXME: Sort due list on date
    mit_list = [mit for mit in mit_list if mit not in delegated_list]
    # Get flagged emails
    flagged_list = applewrap.get_flagged_emails(conf.mail_client)

    # Produce output
    parts = [wp.html_header('Overview', 'TextTasks')]
    if not mit_list and not flagged_list:
        parts.append("<p>No MIT's, due tasks, or flagged emails found :-D</p>")
    else:
        mailscript = '''
        <script>
            function open_mail(client, msgid) {
                if (client === "outlook") {
                    cmd = "mdfind com_microsoft_outlook_recordID == " + msgid + " -0 | xargs -0 open";
                } else {
                    // Assume Mail.app
                    cmd = "open message://%3C" + msgid + "%3E"
                }
                obj = TextMate.system(cmd, null);
            }
        </script>
        '''
        parts.append(mailscript)

        parts.append('<h2>Tasks</h2>')
        parts.extend([format_output(mit) for mit in mit_list])

        parts.append('<h2>Due soon</h2>')
        parts.extend([format_output(due) for due in due_list])

        parts.append('<h2>Delegated</h2>')
        parts.extend([format_output(delegated) for delegated in delegated_list])

        parts.append('<h2>Flagged emails</h2>')
        parts.extend([format_flagged_email(flagged) for flagged in flagged_list])

    parts.append(wp.html_footer())
    return "\n".join(parts)




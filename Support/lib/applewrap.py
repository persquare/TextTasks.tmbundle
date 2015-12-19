#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# 2014-08-20
# Development moved to TextTasks.tmbundle
#

import sys
from Foundation import NSAppleScript
import subprocess
from subprocess import Popen, PIPE

def osascript(script):
    """ Run an applescript and return the output.

    Make a list ['osascript', '-e', '<script line1>, '-e', <'script line2'>, ...]
    and pass it to subprocess.check_output.
    """

    prefixed_lines = [['-e', x] for x in script.split('\n') if x != '']
    # The list comprehension for double lists should be regarded as
    # for x in prefixed_lines:
    #     for y in x:
    #       list.append(y)
    flat_list = [y for x in prefixed_lines for y in x]
    cmd = ['osascript'] + flat_list

    try:
        result = subprocess.check_output(cmd)
        if result < 0:
            print >>sys.stderr, "Child was terminated by signal", -result
    except Exception as e:
        print >>sys.stderr, "Execution failed:", e
        result = None

    return result

def convert_to_html(raw_text):
    cmd = ['textutil', '-stdin', '-stdout', '-convert', 'html']
    p = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate(raw_text)
    # print stderr
    # print stdout
    return stdout

class Mail(object):
    """Class to simplify workin with Mail"""

    def __init__(self):
        super(Mail, self).__init__()

    def get_flagged_emails(self, flag_index=0):
        """Return a list of (from, subject, message_id) tuples of mails flagged with _flag_index_."""

        script = """
            set flaggedList to {}
            tell application "Mail"
            	set theMessages to every message in inbox whose flagged status is true and flag index is %d
            	repeat with thisMessage in theMessages
            		set fromMsg to (sender of thisMessage as string)
            		set subjMsg to (subject of thisMessage as string)
            		set msgID to message id of thisMessage
            		set info to {fromMsg, subjMsg, msgID}
            		copy info to end of flaggedList
            	end repeat
            end tell
            return flaggedList
        """ % flag_index
        applescript = NSAppleScript.alloc().initWithSource_(script)
        desc, status = applescript.executeAndReturnError_(None)
        if desc == None:
            return []
        mailcount = desc.numberOfItems()
        res = [[desc.descriptorAtIndex_(i).descriptorAtIndex_(j).stringValue() for j in range(1,4)] for i in range(1, mailcount+1)]
        return res


class Notes(object):
    """Class to simplify working with Notes"""

    def __init__(self):
        super(Notes, self).__init__()
        # Set default account and folder from our POW (not as seen by Reminders)
        self.account = u'iCloud'
        self.folder = u'Notes'

    def run(self):
        print app.add_new_note(u'Test')
        # print app.get_defaults()
        # print app.get_accounts()
        # print app.get_lists(u'Ericsson')
        # iCloud_lists = app.get_lists(u'iCloud')
        # print app.add_new_task(u'iCloud', iCloud_lists[2])

    def add_new_note(self, note=None, account=None, folder=None, title='Note service'):
        if not note:
            return "Nothing added"

        #print note
        #note = convert_to_html(note) # This is not valid any more
        #print note
        if not account:
            account = self.account
        if not folder:
            folder = self.folder

        script = """
        set noteText to do shell script "echo " & "%s" & " | /usr/bin/textutil -stdin -stdout -convert html"
    	tell application "Notes"
    		tell folder named "%s" of account named "%s"
    				make new note with properties {name:"%s", body: noteText}
    		end tell
    	end tell
        """ % (note, folder, account, title)

        return osascript(script)


class Reminders(object):
    """Class to simplify working with Reminders"""

    def __init__(self):
        super(Reminders, self).__init__()
        # Set default account and list from our POW (not as seen by Reminders)
        self.account = u'iCloud'
        self.list = u'Test'

    def run(self):
        print app.get_defaults()
        print app.get_accounts()
        print app.get_lists(u'Ericsson')
        iCloud_lists = app.get_lists(u'iCloud')
        print app.add_new_task(u'iCloud', u'Inbox:')

    def add_new_task(self, account=None, list=None, title='New todo', note=None, due_date=None):
        """
        Add a new task to Reminders.app
        """
        props = 'name:"%s"' % title
        if note:
            props += ', body:"%s"' % note
        if due_date:
            props += ', due date:date "%s"' % due_date

        script = """
    	tell application "Reminders"
            tell list named "%s" of account named "%s"
                make new reminder with properties {%s}
            end tell
        end tell
        """ % (list, account, props)

        return osascript(script)

    def get_defaults(self):
        """
        Get the default account and its default list from Reminders.app
        Returns a tuple (account, list) that is guaranteed to be valid
        Known issues: The default list might not be in the default account?
        """
        script = """
        tell application "Reminders"
        	return (name of default account, name of default list)
        end tell
        """
        result = osascript(script).decode(encoding='UTF-8')
        account, list = result.split(',')
        return (account.strip(), list.strip())

    def get_accounts(self):
        """
        Get the list of accounts in Reminders.app
        Returns a list of account names
        """
        script = """tell application "Reminders" to return name of accounts"""
        raw = osascript(script).decode(encoding='UTF-8').split(',')
        account_list = [x.strip() for x in raw]
        return account_list

    def get_lists(self, account=None):
        """
        Get lists in 'account' from Reminders.app,
        falls back to default account if no account is specified.
        Returns a list of list names
        """
        if not account:
            account, _= self.get_defaults()

        script = """tell application "Reminders" to return name of lists in account named "%s" """ % account

        raw = osascript(script).decode(encoding='UTF-8').split(',')
        lists = [x.strip() for x in raw]

        return lists

def usage():
    print "Error"
    print "Invoked as: ", sys.argv


if __name__ == '__main__':
    invocation_name = sys.argv[0]
    arg_list = sys.argv[1:]
#    app  = Reminders()
#    mappings = {'add_new_task_to_reminders': app.add_new_task,
#     'get_default_account_and_list_from_reminders': app.get_defaults,
#     'get_lists_in_account_from_reminders': app.get_lists,
#    }
    print invocation_name
    print arg_list

#    mappings.get(invocation_name, app.run)(*arg_list)

    # app = Notes()
    # app.run()

    app = Reminders()
    app.run()

    # print app.get_defaults()
    # print app.get_accounts()
    # print app.get_lists(u'Ericsson')
    # iCloud_lists = app.get_lists(u'iCloud')
    # print app.add_new_task(u'iCloud', iCloud_lists[2])

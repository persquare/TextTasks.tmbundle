#!/usr/bin/env python

import sys
import os
import re

"""inbox: a command to add tasks to the top level inbox"""


USAGE_TEMPLATE = """
%s <task> [URI]
"""

TASK_REGEX = r'(.*)((?:file|https?|txmt)://.+)?'



if len(sys.argv) < 2:
    sys.stderr.write(USAGE_TEMPLATE % os.path.basename(sys.argv[0]))
    exit(1)
    
arg_string = " ".join(sys.argv[1:])

match = re.match(TASK_REGEX, arg_string)
if not match:
    sys.stderr.write("Can't parse %s" % arg_string)
    exit(1)
    
task = match.group(1)
ref = match.group(2) # Possibly 'None'
if ref:
    ref = ' ' + ref
else:
    ref = ''

list_dir = os.environ.get('TTS_LISTS_DIR', '$HOME/Dropbox/Lists')
inbox_file = os.environ.get('TTS_INBOX_FILE', 'inbox.todo')
inbox_path = os.path.join(list_dir, inbox_file)

cmd = "echo - %s%s >> %s" % (task, ref, inbox_path)
os.system(cmd)


     
    
    
    
    
    
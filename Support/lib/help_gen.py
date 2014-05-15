#!/usr/bin/env python
# encoding: utf-8

"""
This module generates documentation for a TextMate bundle by parsing the .tmCommand files.
"""

import os
import sys
import re

try:
    import biplist as plistlib
except:
    import plistlib

def parse_keycode(keycode):
    # a => A
    # A => ⇧A
    # ~ => ⌥
    # ^ => ⌃
    # @ => ⌘
    # $ ⌅ ⎋ ⇥
    # *
    mappings = {
        u'~':u'⌥',
        u'^':u'⌃',
        u'@':u'⌘',
        u'\x0A':u'↩',
        u'\x08':u'⇥'
    }
    printable = []
    shifted = False
    keycode = list(keycode)
    key = keycode.pop().decode('utf-8')
    key = mappings.get(key, key)
    printable.append(key.upper())
    if key >= 'A' and key <= 'Z':
        shifted = True
        
    while keycode:        
        key = keycode.pop().decode('utf-8')
        printable.append(mappings.get(key, u'¿'))

    if shifted:
        printable.append(u'⇧')
                
    printable.reverse()
    
    return printable

def commandlist(cmd_dir):
    commands = [];
    errors = []
    for file in os.listdir(cmd_dir):
        path = unicode(os.path.join(cmd_dir, file), 'utf-8')
        pl = plistlib.readPlist(path)
        try:
            raw_combo = pl.get(u'keyEquivalent', u'')
            name = pl.get(u'name', u'NONAME')
            docstring = extract_docstring(pl.get(u'command', u''))
            commands.append((raw_combo, name, docstring))
        except:
            print "Unexpected error:", sys.exc_info()[0]
            #print raw_combo, name
            print type(path), path
            errors.append(path)
            raise
    return commands, errors
    
def extract_docstring(string):
    DOCSTRING = r'\s*#!.+?python.*?"""(.*?)"""'
    match = re.match(DOCSTRING, string, re.DOTALL)
    if match:
        return match.group(1)
    return u''
    
    
def generate_keyboard_shortcut_docs(cmd_dir):    
    # Auto-generate keyboard shortcut list
    print u'<table><tr><th>Keys</th><th>Command</th><th>Comment</th></tr>\n'.encode('utf-8')

    cmds, errors = commandlist(cmd_dir)
    for (raw_combo, cmd_name, docstring) in cmds:
        if not raw_combo:
            continue
        combo = parse_keycode(raw_combo)
        help = u''.join(combo)
        if not help.strip():
            continue
        line = u'<tr><td>%s</td><td>%s</td><td>%s</td></tr>\n' % (help, cmd_name, docstring)
        
        ## NOTE!
        ## THIS is where we need to ENCODE (= turn a unicode string into bytes)
        ## AND specify the format to use (UTF-8) in the encoding process,
        ## the default encoding is ASCII which is SOO WRONG for unicode strings.
        print line.encode('utf-8')
        
    print u'</table>'.encode('utf-8')

    
if __name__ == '__main__':
    CMD_DIR = '/Users/eperspe/Source/FOSS/TextTasks.tmbundle/Commands'
    
    cmds, error_files = commandlist(CMD_DIR)
    print u'Command files:'
    for t in cmds:
        print type(t[0]), t[0], ' : ', type(t[1]), t[1]
    print u'Error in files:'
    print error_files
    for f in error_files:
        print f
    #
    generate_keyboard_shortcut_docs(CMD_DIR)   
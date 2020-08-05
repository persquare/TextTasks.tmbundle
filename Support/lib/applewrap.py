#!/usr/bin/env python3

import subprocess
import re

outlook = """
        set flaggedList to {}
        tell application "Microsoft Outlook"
        	set theMessages to messages of inbox whose todo flag is (not completed)
        	repeat with thisMessage in theMessages
        		set theSender to sender of thisMessage
        		set fromMsg to address of theSender
        		set subjMsg to subject of thisMessage
        		set msgID to id of thisMessage as string
        		set info to {quoted form of fromMsg, quoted form of subjMsg, quoted form of msgID}
        		copy info to end of flaggedList
        	end repeat
            copy "" as string to end of flaggedList
        end tell
        return flaggedList
    """

mail = """
        set flaggedList to {}
        tell application "Mail"
        	set theMessages to every message in inbox whose flagged status is true and flag index is 0
        	repeat with thisMessage in theMessages
        		set fromMsg to (sender of thisMessage as string)
        		set subjMsg to (subject of thisMessage as string)
        		set msgID to message id of thisMessage
        		set info to {quoted form of fromMsg, quoted form of subjMsg, quoted form of msgID}
        		copy info to end of flaggedList
        	end repeat
            copy "" as string to end of flaggedList
        end tell
        return flaggedList
    """

def get_flagged_emails(client):

    script = mail if client == 'mail' else outlook

    p = subprocess.Popen(['osascript', '-'],
                         stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE,
                         universal_newlines=True)
    stdout, stderr = p.communicate(script)

    if p.returncode:
        return (f"Error {p.returncode}", stderr, "error")

    items = list(m.group(1) for m in re.finditer(r"'(.+?)',\s*", stdout))
    res = []
    while items:
        res.append(tuple(items[:3]))
        items = items[3:]

    return res

if __name__ == '__main__':
    print(get_flagged_emails('mail'))

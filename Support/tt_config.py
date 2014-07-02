##
# This is the TextTasks settings file
# 

##
# Directories to search for files with above extensions
#
# ---- IMPORTANT! ----------------------------------------- #
# Please modify PROJECT_DIRS below and add paths to         #
# directories where TextTasks should look for task files.   #
# Environment variables such as HOME, etc. are allowed #
# in paths, but relative paths are not allowed.             #
# --------------------------------------------------------- #
PROJECT_DIRS = ['${HOME}']

##
# This is a list of the extension recognized by TextTasks
#
FILE_EXTS = ['.todo', '.tasks']

##
# The dedicated inbox file
#
INBOX = '${HOME}/inbox.todo'

##
# The tags that populate the tag pop-up list
#
TAGS = ['next', 'remind', 'due']

##
# Quic-list tags and any tag with a date at most n days ahead 
#
QUICK_LIST_TAGS = ['next']
QUICK_LIST_DAYS_AHEAD = 1

##
# Special sections
#
ARCHIVE_SECTION = Archive
REFERENCE_SECTION = References
ISSUE_SECTION = Bugs

##
# Enable/disable TextTasks helpers
#
ENABLE_INBOX_CLI = False
ENABLE_INBOX_APP = False
ENABLE_MAIL_APP_RULES = False




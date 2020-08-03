import os
from collections import namedtuple

Config = namedtuple('Config', "project_dirs file_exts mail_client")

def config():
    project_dirs = os.environ.get('TT_PROJECT_DIRS', 'PWD').split(':')
    file_exts = os.environ.get('TT_FILE_EXTS', '.todo').split(',')

    current_dir = os.environ.get('TM_DIRECTORY')
    if current_dir and current_dir not in project_dirs:
        project_dirs.insert(0, current_dir)

    mail_client = os.environ.get('TT_MAIL_CLIENT', 'mail')

    return Config(project_dirs, file_exts, mail_client)


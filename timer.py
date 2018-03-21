import sys
import os
from collections import namedtuple
import time

LOGS_DIR_PATH = '/home/pandu/projects/freelance-timer/logs/'
PROJECTS_LIST_PATH = '/home/pandu/projects/freelance-timer/projects.txt'
C_DIR_PATH = '/home/pandu/c/'

# Project = namedtuple('Project', 'path name')


def get_project_paths():
    with open(PROJECTS_LIST_PATH, 'r') as f:
        paths = [line.strip() for line in f]
        return {path.split('/')[-1]: path for path in paths}

def main(args):
    assert len(args) == 2
    command, project_name = args
    project_paths = get_project_paths()
    assert project_name in project_paths
    if command == 'start':
        start(project_name)
    elif command == 'stop':
        stop(project_name)
    else:
        print('bad command name')

def start(name):
    project_paths = get_project_paths()
    os.chdir(C_DIR_PATH)
    try:
        os.symlink(project_paths[name], name)
    except FileExistsError:
        pass
    os.chdir(LOGS_DIR_PATH)
    append_entry(name, 'start\t' + time.time())

def stop(name):
    project_paths = get_project_paths()
    os.chdir(C_DIR_PATH)
    try:
        os.unlink(name)
    except FileExistsError:
        pass
    os.chdir(LOGS_DIR_PATH)
    append_entry(name, 'stop\t' + time.time())

def append_entry(path, text):
    with open(path, 'a') as f:
        f.write(text + '\n')

if __name__ == '__main__':
    main(sys.argv[1:])

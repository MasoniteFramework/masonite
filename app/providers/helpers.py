import os
import sys

def controller():
    if os.path.isfile('app/http/controllers/' + sys.argv[2] + '.py'):
        print '\033[95m' + sys.argv[2] + ' Controller Exists!' + '\033[0m'
    else:
        f = open('app/http/controllers/' + sys.argv[2] + '.py', 'w+')
        f.write("''' A Module Description '''\n")
        f.write('from app.http.providers.view import view\n\n')
        f.write('class ' + sys.argv[2] + '(object):\n')
        f.write("    ''' Class Docstring Description '''\n\n")
        f.write('    def __init__(self):\n')
        f.write('        pass\n')

        print '\033[92m' + sys.argv[2] + ' Created Successfully!' + '\033[0m'

def view():
    
    if os.path.isfile('resources/templates/' + sys.argv[2] + '.blade.html'):
        print '\033[95m' + sys.argv[2] + ' View Exists!' + '\033[0m'
    else:
        f = open('resources/templates/' + sys.argv[2] + '.blade.html', 'w+')
        print '\033[92m' + sys.argv[2] + ' View Created Successfully!' + '\033[0m'

def serve():
    from subprocess import call
    call(["gunicorn", "-w 1", "mine:app"])

def install():
    from subprocess import call
    call(["pip", "install", "-r", "requirements.txt"])

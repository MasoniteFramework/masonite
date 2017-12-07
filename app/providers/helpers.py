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

def model():
    if not os.path.isfile('app/' + sys.argv[2] + '.py'):
        f = open('app/' + sys.argv[2] + '.py', 'w+')

        f.write("''' A " + sys.argv[2] + " Database Module '''\n")
        f.write('from peewee import *\n')
        f.write('from config import database\n\n')
        f.write("db = database.engines['default']\n\n")
        f.write("class "+sys.argv[2]+"(Model):\n    ")
        f.write("# column = charField()\n\n")
        f.write("    class Meta:\n")
        f.write("        database = db\n\n")
        f.write("db.connect()\n")

        print '\033[92mModel Created Successfully!\033[0m'
    else:
        print '\033[95mModel Already Exists!\033[0m'

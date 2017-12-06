import os
import sys

if (sys.argv[1] == 'make:controller'):
    if (os.path.isfile('app/http/controllers/' + sys.argv[2] + '.py')):
        print('\033[95m'+sys.argv[2] + ' Controller Exists!' + '\033[0m')
    else:
        file = open('app/http/controllers/' + sys.argv[2] + '.py', 'w+')
        file.write('from app.http.providers.view import view\n\n')
        file.write('class ' + sys.argv[2] + '():\n')
        file.write('\tpass')

        print('\033[92m' + sys.argv[2] + ' Created Successfully!' + '\033[0m')

if (sys.argv[1] == 'make:view'):
    if (os.path.isfile('resources/templates/' + sys.argv[2] + '.blade.html')):
        print('\033[95m'+sys.argv[2] + ' View Exists!' + '\033[0m')
    else:
        file = open('resources/templates/' + sys.argv[2] + '.blade.html', 'w+')
        print('\033[92m' + sys.argv[2] + ' View Created Successfully!' + '\033[0m')


if (sys.argv[1] == 'serve'):
    from subprocess import call
    call(["gunicorn", "-w 1", "mine:app"])

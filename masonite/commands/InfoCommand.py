import math
import platform
from subprocess import check_output
import sys

from cleo import Command
import psutil
from tabulate import tabulate

from masonite.info import VERSION


class InfoCommand(Command):
    """
    Displays environment info for debugging

    info
    """

    def handle(self):
        rows = []

        rows.append(['System Information', self._get_system_info()])
        mem = math.ceil(psutil.virtual_memory().total / 1024 / 1024 / 1024.0)
        rows.append(['System Memory', str(mem) + ' GB'])
        rows.append(['Python Version', self._get_python_info()])
        rows.append(['Virtual Environment', self._check_virtual_environment()])
        rows.append(['Masonite Version', VERSION])

        self.info('')
        self.info(tabulate(rows, headers=['Environment Information', '']))
        self.info('')

    def _get_python_info(self):
        py_version = platform.python_version()
        py_implementation = platform.python_implementation()
        return py_implementation + ' ' + py_version

    def _check_virtual_environment(self):
        if hasattr(sys, 'real_prefix'):
            return u'\u2713'  # currently running in virutal env
        return 'X'

    def _get_system_info(self):
        bits, _ = platform.architecture()
        operating_system, _, _, _, arch, _ = platform.uname()

        if operating_system.lower() == 'darwin':
            operating_system = 'MacOS'
        return '{} {} {}'.format(operating_system, arch, bits)

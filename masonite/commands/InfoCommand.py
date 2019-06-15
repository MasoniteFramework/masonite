"""Displays Information Command."""
import math
import os
import platform
import sys
import psutil

from cleo import Command
from tabulate import tabulate

from masonite.__version__ import __version__


class InfoCommand(Command):
    """
    Displays environment info for debugging.

    info
    """

    def handle(self):
        from masonite_cli.application import application
        rows = []

        rows.append(['System Information', self._get_system_info()])
        mem = math.ceil(psutil.virtual_memory().total / 1024 / 1024 / 1024.0)
        rows.append(['System Memory', str(mem) + ' GB'])
        rows.append(['Python Version', self._get_python_info()])
        rows.append(['Virtual Environment', self._check_virtual_environment()])
        rows.append(['Masonite Version', __version__])
        rows.append(['Craft Version', application._version])

        if 'APP_ENV' in os.environ:
            rows.append(['APP_ENV', os.environ.get('APP_ENV')])

        if 'APP_DEBUG' in os.environ:
            rows.append(['APP_DEBUG', os.environ.get('APP_DEBUG')])

        self.info('')
        self.info(tabulate(rows, headers=['Environment Information', '']))
        self.info('')

    def _get_python_info(self):
        py_version = platform.python_version()
        py_implementation = platform.python_implementation()
        return py_implementation + ' ' + py_version

    def _check_virtual_environment(self):
        if hasattr(sys, 'real_prefix') or 'VIRTUAL_ENV' in os.environ:
            return u'\u2713'  # currently running in virtual env
        return 'X'

    def _get_system_info(self):
        bits, _ = platform.architecture()
        operating_system, _, _, _, arch, _ = platform.uname()

        if operating_system.lower() == 'darwin':
            operating_system = 'MacOS'
        return '{} {} {}'.format(operating_system, arch, bits)

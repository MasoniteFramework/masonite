import math
import os
import platform
from subprocess import check_output
import sys

from cleo import Command

from masonite.info import VERSION


class InfoCommand(Command):
    """
    Displays environment info for debugging

    info
    """

    def handle(self):
        operating_system, system_info  = self._get_system_info()
        memory_info = self._get_mem_info(operating_system.lower())
        py_details = self._get_python_info()
        virtual = self._check_virtual_environment()

        self.info('Masonite Version: {0:>37}'.format(VERSION))
        self.info('Python Version: {0:>39}'.format(py_details))
        self.info('Virtual Environment: {0:>34}'.format(virtual))
        self.info('System Information: {0:>35}'.format(system_info))
        self.info('System Memory: {0:>40}'.format(memory_info))

        # self.info('Python Version %25s'.format(pl.python_version()))

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
        op_sys, _, _, _, arch, _ = platform.uname()

        if op_sys.lower() == 'darwin':
            op_sys = 'MacOS'
        return op_sys, '{} {} {}'.format(op_sys, arch, bits)

    def _get_mem_info(self, operating_system):
        if operating_system == 'macos':
            hardware = check_output(['system_profiler', 'SPHardwareDataType'])
            for line in hardware.decode('utf-8').split('\n'):
                if ' Memory: ' in line:
                    return line.split(': ')[1]
        elif operating_system == 'linux':
            # TODO: test this on Linux
            output = check_output(['free']).decode('utf-8').split('\n')
            return math.ceil(int(output.split()[1]) / 1024 / 1024.0) + ' GB'
        else:
            # TODO: test this on Windows
            # mem_total = os.popen('mem | find "total"').readlines()
            # memory = int(mem_total[0].split()[0])
            return '0 GB'
        # terminal_width = check_output(['tput', 'cols']).decode('utf-8').strip()

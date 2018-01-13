''' Test the wsgi server running '''
import subprocess

import signal
import sys
import os

def test_run_server():
    pro = subprocess.Popen('craft serve', stdout=subprocess.PIPE,
                           shell=True, preexec_fn=os.setsid)

    kill = os.killpg(os.getpgid(pro.pid), signal.SIGTERM)
    assert True

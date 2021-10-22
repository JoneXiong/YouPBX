#!/usr/bin/env python
import os
import sys
import subprocess

from config import event_socket_conf as fsc

if __name__ == "__main__":
    PROJECT_ROOT = os.path.realpath(os.path.dirname(__file__))
    sys.path.insert(0, os.path.join(PROJECT_ROOT, 'lib'))
    if 'runserver' in sys.argv:
        if sys.platform in ['win32', 'cygwin']:
            cmd = './proxy/win/fs_agw'
        else:
            cmd = './proxy/linux/fs_agw'
        p = subprocess.Popen(cmd + ' -fshost %s -fsport %s -pass %s' % (fsc['host'], fsc['port'], fsc['pwd']))

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "apps.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)

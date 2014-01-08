#! /usr/bin/env python
'''Upload sysmon to remote machine, start it, maybe for some time duration,
maybe not'''

import utils as ut
from fabric.api import execute
from fabric.operations import put

def main():
    """docstring for main"""
    settings = ut.options()
    execute(ut.rmdir, settings.test_name, hosts = settings.hosts)

if __name__ == '__main__':
    main()

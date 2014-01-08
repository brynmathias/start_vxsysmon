#! /usr/bin/env python
'''Upload sysmon to remote machine, start it, maybe for some time duration,
maybe not'''

import utils as ut
from fabric.api import execute
def main():
    """docstring for main"""
    settings = ut.options()
    execute(ut.stop_sysmon, hosts = settings.hosts)

if __name__ == '__main__':
    main()

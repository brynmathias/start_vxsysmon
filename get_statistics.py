#! /usr/bin/env python
'''Upload sysmon to remote machine, start it, maybe for some time duration,
maybe not'''

import utils as ut
from fabric.api import execute
import fabric
def main():
    """docstring for main"""
    settings = ut.options()
    fabric.api.env.warn_only = True
    for h in settings.hosts:
        execute(ut.get_sysmon_logs, settings = settings, hostname = h, hosts
            = [h])

if __name__ == '__main__':
    main()

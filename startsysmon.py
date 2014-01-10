#! /usr/bin/env python
'''Upload sysmon to remote machine, start it, maybe for some time duration,
maybe not'''

import utils as ut
from fabric.api import execute
from fabric.operations import put
VXSYSMON_PATH = "./vxsysmon"
def main():
    """docstring for main"""
    settings = ut.options()

    ut.make_run_script(settings)

    execute(ut.mkdir, settings.test_name, hosts = settings.hosts)

    execute(put, VXSYSMON_PATH, "./"+settings.test_name+"/"+VXSYSMON_PATH,
            hosts = settings.hosts)

    execute(put, "./start_sysmon.sh", "./"+settings.test_name+"/start_sysmon.sh"
            , hosts = settings.hosts)
    execute(ut.start_sysmon, settings.test_name, hosts = settings.hosts)

    print settings

if __name__ == '__main__':
    main()

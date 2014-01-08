#! /usr/bin/env python
'''Utils folder, tools to send vxsysmon to remote machines, start it, stop it,
grab the results and plot them locally'''

import fabric as fab
import datetime as dt
import argparse as ap






def options():
    """set up argparse, parse the options and return the stuffs"""
    parser = ap.ArgumentParser(description="Start vxsysmon on remote machines")

    parser.add_argument("--hosts", "-H", type = str, default = [], nargs='+',
                        help = "List of hosts you wish to start or stop" +
                        "vxsysmon on", dest = "hosts")

    parser.add_argument("--test", "-T", type = str, default =
            dt.datetime.now().strftime("%Y-%m-%d-%H-%M"), dest = "test_name",
            help = "Name of test, defaults to current date+time")

    parser.add_argument("--runtime", "-t", type = int, default = None, dest =
            "runtime", help = "Amount of time we want to run for in hours")

    return parser.parse_args()
def mkdir(dir_name):
    """mkdir: make a dir on a machine"""
    fab.api.run("mkdir "+ dir_name)

def rmdir(dir_name):
    """mkdir: make a dir on a machine"""
    fab.api.run("rm -rf "+ dir_name)


def copy_to_hosts(remote_path = None, local_path = None):
    """copy_to_hosts: copy some file to the remote machine"""
    fab.operations.put( local_path, remote_path)

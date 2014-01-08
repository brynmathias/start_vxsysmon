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




def mkdir(dir_name = None):
    """mkdir: make a dir on a machine"""
    fab.api.run("mkdir "+ dir_name)

def rmdir(dir_name = None):
    """rmdir: remove a dir on a machine"""
    fab.api.run("rm -rf "+ dir_name)

def start_sysmon(vx_sysmon = None):
    """start_sysmon starts the sysmon process"""
    fab.api.sudo("chmod +x " + vx_sysmon)
    fab.api.run("nohup " + vx_sysmon + " &")

def stop_sysmon():
    """stop_sysmon"""
    fab.api.run("killall vxsysmon")

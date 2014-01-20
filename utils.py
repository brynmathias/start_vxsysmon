#! /usr/bin/env python
'''Utils folder, tools to send vxsysmon to remote machines, start it, stop it,
grab the results and plot them locally'''

import fabric as fab
import datetime as dt
import argparse as ap
from os.path import expanduser




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
    fab.api.env.always_use_pty = False
    fab.api.env.warn_only = True
    return parser.parse_args()


def get_sysmon_logs(settings = None, hostname = None):
    """get_sysmon_logs: get the logs from the remote machines, put them in
    subfolders of the host name, inside a folder with the test name"""
    if "@" in hostname:
        hostname = hostname.split("@")[1]
    local_dir = "{home}/perf_test_results/{test}/{host}".format(home =
        expanduser("~"), test = settings.test_name, host = hostname)

    fab.api.local("mkdir -p "+local_dir)

    for f in fab.api.run("ls {test}".format(test =
        settings.test_name)).split("\n"):
        fab.operations.get(settings.test_name+"/"+f, "{local}/{fi}".format(
            local = local_dir, host = hostname, fi = f))

def mkdir(dir_name = None):
    """mkdir: make a dir on a machine"""
    fab.api.run("mkdir "+ dir_name)

def rmdir(dir_name = None):
    """rmdir: remove a dir on a machine"""
    fab.api.env.warn_only = True
    fab.api.run("rm -rf "+ dir_name)

def start_sysmon(vx_sysmon_path = None):
    """start_sysmon starts the sysmon process"""
    fab.api.env.always_use_pty = True
    with fab.api.cd(vx_sysmon_path):
        fab.api.sudo("chmod +x ./vxsysmon")
        fab.api.sudo("chmod +x ./start_sysmon.sh")
    fab.api.env.always_use_pty = False
    with fab.api.cd(vx_sysmon_path):
        fab.api.run("nohup ./start_sysmon.sh >& /dev/null < /dev/null &",
                pty = True)

def stop_sysmon():
    """stop_sysmon"""
    fab.api.run("killall vxsysmon")


def make_run_script(settings = None):
    """make_run_script make a script that runs the vxsysmon,
    sleeps if necessary"""
    script = open("./start_sysmon_tmp.sh",'r')
    script = script.read()
    script = script.replace('TEST_TMP', settings.test_name)
    if settings.runtime is not None:
        script = script.replace('TESTTIME', "sleep {time}".format(time =
            settings.runtime*3600))
        script = script.replace('TESTEND', "killall vxsysmon")
    else:
        script = script.replace('TESTTIME', "")
        script = script.replace('TESTEND',  "")

    out_file = open("./start_sysmon.sh",'w')
    out_file.write(script)
    out_file.close()

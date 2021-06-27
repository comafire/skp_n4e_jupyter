import os, sys, json, re
from pprint import pprint

def run_with_exit(c, cmd, pty=False):
    res = c.run(cmd, warn=True, pty=pty)
    if res.failed:
        print("Fail to Run: {}".format(res.stderr.strip()))
        sys.exit(-1)
    return res.stdout.strip()

def run_without_exit(c, cmd):
    res = c.run(cmd, warn=True)
    if res.failed:
        print("Fail to Run: {}".format(res.stderr.strip()))
    return res.stdout.strip()

def is_macos(c):
    uname = run_with_exit(c, "uname")
    if "Darwin" in uname:
        return True
    return False

def is_ubuntu(c):
    uname = run_with_exit(c, "uname -a")
    if "Ubuntu" in uname:
        return True
    return False

def get_ubuntu_release(c):
    # os: lsb_release -si
    # release: lsb_release -sr
    if is_ubuntu(c):
        return run_with_exit(c, "lsb_release -sr")
    return None

def get_ubuntu_codename(c):
    # os: lsb_release -si
    # release: lsb_release -sr
    # codename: lsb_release -sc
    if is_ubuntu(c):
        return run_with_exit(c, "lsb_release -sc")
    return None

def mkdir_usr(c, base):
    path_usr = f"{base}/usr"
    cmd = f"mkdir -p {path_usr}"
    run_with_exit(c, cmd)


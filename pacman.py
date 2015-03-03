#
# python-pacman - (c) Jacob Cook 2015
# Licensed under GPLv3
#

import subprocess


def install(packages, needed=True):
    # Install package(s)
    s = pacman("-S", packages, ["--needed" if needed else None])
    if s["code"] != 0:
        raise Exception("Failed to install: %s" % str(s["stderr"]))

def refresh():
    # Refresh the local package information database
    s = pacman("-Sy")
    if s["code"] != 0:
        raise Exception("Failed to refresh database: %s" % str(s["stderr"]))

def upgrade(packages=[]):
    # Upgrade packages; if unspecified upgrade all packages
    if packages:
        install(packages)
    else:
        s = pacman("-Su")
    if s["code"] != 0:
        raise Exception("Failed to upgrade packages: %s" % str(s["stderr"]))

def remove(packages, purge=False):
    # Remove package(s), purge its files if requested
    s = pacman("-R%s" % ("n" if purge else ""), packages)
    if s["code"] != 0:
        raise Exception("Failed to remove: %s" % str(s["stderr"]))

def get_installed():
    # List all installed packages
    interim = {}
    s = pacman("-Q")
    if s["code"] != 0:
        raise Exception("Failed to get installed list: %s" % str(s["stderr"]))
    for x in s["stdout"].split('\n'):
        if not x.split():
            continue
        x = x.split(' ')
        interim[x[0]] = {"id": x[0], "version": x[1], "upgradable": False}
    s = pacman("-Qu")
    if s["code"] != 0:
        raise Exception("Failed to get upgradable list: %s" % str(s["stderr"]))
    for x in s["stdout"].split('\n'):
        if not x.split():
            continue
        x = x.split(' -> ')
        name = x[0].split(' ')[0]
        if interim.has_key(name):
            r = interim[name]
            r["upgradable"] = x[1]
            interim[name] = r
    results = []
    for x in interim:
        results.append(interim[x])
    return results

def get_available():
    # List all available packages
    results = []
    s = pacman("-Sl")
    if s["code"] != 0:
        raise Exception("Failed to get available list: %s" % str(s["stderr"]))
    for x in s["stdout"].split('\n'):
        if not x.split():
            continue
        x = x.split(' ')
        results.append({"id": x[1], "repo": x[0], "version": x[2]})
    return results

def get_info(package, installed=True):
    # Get package information from database
    interim = []
    s = pacman("-Qi" if installed else "-Si", package)
    if s["code"] != 0:
        raise Exception("Failed to get info: %s" % str(s["stderr"]))
    for x in s["stdout"].split('\n'):
        if not x.split():
            continue
        if ':' in x:
            x = x.split(':')
            interim.append((x[0].strip(), x[1].strip()))
        else:
            data = interim[-1]
            data = (data[0], data[1]+"  "+x.strip())
            interim[-1] = data
    result = {}
    for x in interim:
        result[x[0]] = x[1]
    return result

def needs_for(packages):
    # Get list of not-yet-installed dependencies of these packages
    s = pacman("-Sp", packages, ["--print-format", "%n"])
    if s["code"] != 0:
        raise Exception("Failed to get requirements: %s" % str(s["stderr"]))
    return [x for x in s["stdout"].split('\n') if x]

def depends_for(packages):
    # Get list of installed packages that depend on these
    s = pacman("-Rpc", packages, ["--print-format", "%n"])
    if s["code"] != 0:
        raise Exception("Failed to get depends: %s" % str(s["stderr"]))
    return [x for x in s["stdout"].split('\n') if x]

def is_installed(package):
    # Return True if the specified package is installed
    return pacman("-Q", package)["code"]==0

def pacman(flags, pkgs=[], eflgs=[]):
    # Subprocess wrapper, get all data
    if not pkgs:
        cmd = ["pacman", "--noconfirm", flags]
    elif type(pkgs) == list:
        cmd = ["pacman", "--noconfirm", flags, ' '.join(pkgs)]
    else:
        cmd = ["pacman", "--noconfirm", flags, pkgs]
    if eflgs and any(eflgs):
        eflgs = [x for x in eflgs if x]
        cmd += eflgs
    p = subprocess.Popen(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    data = p.communicate()
    data = {"code": p.returncode, "stdout": data[0], 
        "stderr": data[1].rstrip('\n')}
    return data

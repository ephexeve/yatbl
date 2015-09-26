import platform

from os import path as ospath
from os import makedirs
from os import uname
from os import listdir
from os.path import isdir
import re

from sys import exit

from . import config

def get_architecture(): # todo, osx
    arch = platform.architecture()[0]
    return 'linux64' if '64' in arch else 'linux32'

def check_current_version(path):
    if not ospath.exists(path):
        print("Path doesn't exist")
        return False
    if ospath.exists(path + config.file_version):
        version = open(path + config.file_version).read()
        if len(version) == 0:
            return False
        else:
            return version
    return False

def get_platform():
    os_name = uname()[0]
    if os_name == "Darwin":
        os_name = "MacOS"
    return os_name
    
def create_directory(path=None):
    if not path:
        path = config.tor_browser_location
    if ospath.exists(path):
        pass
    else:
        mkdirs(path, 0o700)
    return True

def get_latest(version_list):
    re_remove_experimental = re.compile(r'^\d\.\d[a-zA-Z]')
    stable_versions = [v for v in version_list if not re_remove_experimental.match(v)]
    
    # urg, fix this ugly hack ~pukes
    latest = int(''.join(c for c in stable_versions[0] if c.isdigit()))
    latest_real = version_list[0]
    
    for version in stable_versions:
        stripped = ''.join(c for c in version if c.isdigit())
        tmp = int(stripped)
        if tmp > latest:
            latest = tmp
            latest_real = version
    return version

def check_installed(path=config.tor_browser_path):
    if not os.path.exists(path):
        print("Path doesn't exist")
    files = listdir(path)
    installed_versions = []

    for f in files:
        if isdir(f) and "tor-browser" in f:
            installed_versions.append(f)
    return installed_versions
    

def prompt_version(recommeded_list):
    if len(recommeded_list) <= 0:
        print("Something went wrong")
        exit(1)

    installed_indexes = []
    installed_versions = check_installed()
    for i, r in enumerate(recommeded_list):
        for v in installed_versions:
            if (r in v):
                installed_indexed.append(i)
                print("%d -> %s [installed]" % (i, r))
        print("%d -> %s" % (i, r))
    
    while True:
        version = input("Version to install (blank for lastest stable): ")
        try:
            if not version:
                version = get_latest(recommeded_list)
                print("Auto selected version:", version)
                break
            version = int(version)
            if version in installed_versions:
                print("Version already installed") # todo, enable reinstall
            if version <= len(recommeded_list) and version > -1:
                break
            else:
                print ("Unknown version.")
        except ValueError:
            print("Incorrect version. Try again.")
    return version
                
def prompt_directory():
    while True:
        path = input("Install path (blank for defaul): ")
        if path == "":
            path = config.tor_browser_path
            break
        else:
            if not os.path.exists(path):
                print("Path doesn't exist.")
            elif not os.access(path, os.W_OK):
                print("No privalege to right to %s", path)
            else:
                break
    return path

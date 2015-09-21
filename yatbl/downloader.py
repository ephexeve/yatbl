try:
    import urllib.request as urllib
except: # python < 3
    import urllib

import json
import os
from time import sleep
import subprocess
import hashlib

try:
    from progressbar import ProgressBar, Percentage, Bar, RotatingMarker, \
        FileTransferSpeed, ETA
    has_bar = True
except:
    has_bar = False

from . import utils
from . import config as tbb_config

class Downloader(object):
    """This class takes care of downloading/updating the tor browser"""
    def __init__(self):
        self.path = None
        self.version = None # if not, get the latest
        self.arch = utils.get_architecture()
        self.platform = utils.get_platform()
        
        if has_bar:
            widgets = ['Tor Browser: ', Percentage(), ' ', Bar(marker=RotatingMarker()),\
                            ' ', ETA(), ' ', FileTransferSpeed()]
            self.progressbar = ProgressBar(widgets=widgets)
        else:
            self.progressbar = False
            
    def get_recommended(self, os):
        con = urllib.urlopen(tbb_config.tor_browser_recommended).read()
        recommended = [i for i in json.loads(con.decode()) if os in i] # remove un-needed sys's
        
        return recommended

    def download_files(self):
        version = self.version.split("-")[0]
        url = tbb_config.tor_browser_mirror.format(version)
        url_sig = tbb_config.tor_browser_mirror.format(version)
        
        if self.platform == "Linux":
            if self.arch == "linux32":
                url = url + tbb_config.tor_browser_linux32.format(version)
            else:
                url = url + tbb_config.tor_browser_linux64.format(version)
        else: # macos
            url = url + tbb_config.tor_browser_macos.format(version)

        shasum_url = url + tbb_config.tor_sha_file
        shasumsig_url = url + tbb_config.tor_shasig_file
        
        if self.progressbar:
            print("Downloading Tor browser")

            tor_tar = urllib.urlretrieve(url, reporthook=self.__download_progress)
            self.progressbar.finish()

            print("Downloading signature")
            tor_shasum = urllib.urlretrieve(shasum_asc_url, reporthook=self.__download_progress)
            self.progressbar.finish()
            
            tor_shasig = urllib.urlretrieve(shasum_text_url, reporthook=self.__download_progress)
            self.progressbar.finish()            
        else:
            print("Downloading Tor browser, please wait.")
            tor_tar = urllib.urlretrieve(url)

            print("Downloading signature, please wait.")
            tor_shasum = urllib.urlretrieve(shasum_asc_url)
            tor_shasig = urllib.urlretrieve(shasum_text_url)

        tar_path = tor_tar[0]
        shasum = tor_asc[0]
        shasum_sig = tor_text[0]

        # will exit it verification fails.
        # todo: do something if verification = false
        self.verify(tar_path, shasum, shasum_sig)

    def extract(self, path):
        # todo
        pass
        
    def import_gnupg(self):
        print("Importing Tor's keys")
        homedir = os.path.join(os.path.expanduser("~/"), ".gnupg")

        subprocess.Popen(['/usr/bin/gpg', '--quiet', '--homedir', homedir, \
                          '--import', tbb_config.tor_browser_pub_gpg]).wait()
        
    def verify(self, data, shafile, shasig):
        tar_name = data.split("/")[-1]
        # some parts of this code has been copied from
        # https://github.com/micahflee/torbrowser-launcher/blob/master/torbrowser_launcher/launcher.py#L543
        verified = False
        # check the sha256 file's sig, and also take the sha256 of the tarball and compare
        FNULL = open(os.devnull, 'w')
        gnupg_path = os.path.join(os.path.expanduser("$HOME"), ".gnupg")
        
        process = subprocess.Popen(['/usr/bin/gpg', '--homedir', gnupg_path,\
                                    '--verify', shasig],\
                              stdout=FNULL, stderr=subprocess.STDOUT)
        while process.poll() is None:
            time.sleep(0.01)
            
        if process.returncode == 0:
            tarball_sha256 = hashlib.sha256(open(data, "r").read()).hexdigest()
            for line in open(shafile, "r").readlines():
                if tarball_sha256.lower() in line.lower() and tar_name in line:
                    verified = True

        if not verified: # todo, how to report this?
            print("File was not verified. Exiting.")
            exit(1)
        return verified
        
    def __download_progress(self, count, block_size, total_size):
        if self.progressbar.maxval is None:
            self.progressbar.maxval = total_size
            self.progressbar.start()
        self.progressbar.update(min(count * block_size, total_size))
            
    def start(self):
        recommended = self.get_recommended(utils.get_platform())
        self.version  = utils.prompt_version(recommended)
        self.path = utils.prompt_directory()
        self.download_files()

try:
    import urllib.request as urllib
except: # python < 3
    import urllib

import json
import os

try:
    from progressbar import ProgressBar, Percentage, Bar, RotatingMarker, \
        FileTransferSpeed, ETA
    has_bar = True
except:
    has_bar = False

import gnupg
    
from . import utils
from . import config as tbb_config

class Downloader(object):
    """This class takes care of downloading/updating the tor browser"""
    def __init__(self):
        self.path = None
        self.version = None # if not, get the latest
        self.arch = utils.get_architecture()
        self.platform = utils.get_platform()
        self.gpg = gnupg.GPG()
        
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

    def download_tar(self):
        version = self.version.split("-")[0]
        url = tbb_config.tor_browser_mirror.format(version)
        url_sig = tbb_config.tor_browser_mirror.format(version)
        
        if self.platform == "Linux":
            if self.arch == "linux32":
                url = url + tbb_config.tor_browser_linux32.format(version)
                url_sig = url_sig + tbb_config.tor_browser_linux32_sig.format(version)
            else:
                url = url + tbb_config.tor_browser_linux64.format(version)
                url_sig = url_sig + tbb_config.tor_browser_linux64_sig.format(version)
        else: # macos
            url = url + tbb_config.tor_browser_macos.format(version)
            url_sig = url_sig + tbb_config.tor_browser_macos_sig.format(version)

        if self.progressbar:
            print("Downloading Tor browser")
            tor_bb_tar = urllib.urlretrieve(url, reporthook=self.__download_progress)
            self.progressbar.finish()
            
            print("Downloading signature")
            tor_bb_sig = urllib.urlretrieve(url_sig, reporthook=self.__download_progress)
            self.progressbar.finish()
        else:
            print("Downloading Tor browser, please wait.")
            tor_bb_tar = urllib.urlretrieve(url)

            print("Downloading signature, please wait.")
            tor_bb_tar = urllib.urlretrieve(url)

        downloaded_tar_path = tor_bb_tar[0]
        downloaded_sig_path = tor_bb_sig[0]        

        verified = self.verify(downloaded_tar_path, downloaded_sig_path)
        if not verified:
            print("Could not verify signature!")
            print("Tryint to ")
            print("This could be 2 things:")
            print("1. Someone changed the source code")
            print("2. Something went internaly wrong.")
            print("Check torproject.org to see if there are any news.")
            sys.exit(1)
        else:
            print("File verified!")

    def import_gnupg(self):
        pub_key = self.gpg.import_keys(open(tbb_config.tor_browser_pub_gpg).read())
        if pub_key.imported:
            print("New gpg key imported")
            print("Total imported:", pub_key.imported)
            print("GPG fingerprint:", pub_key.fingerprint[0])
            print("For extra security: Make sure the fingerprint matched the one from torproject.org")
            return True
        return False

    # todo, verify sha256sum too
    def verify(self, data, sig):
        self.import_gnupg()
        pass # todo, verify file
        
    def __download_progress(self, count, block_size, total_size):
        if self.progressbar.maxval is None:
            self.progressbar.maxval = total_size
            self.progressbar.start()
        self.progressbar.update(min(count * block_size, total_size))
            
    def start(self):
        recommended = self.get_recommended(utils.get_platform())
        self.version  = utils.prompt_version(recommended)
        self.path = utils.prompt_directory()
        self.download_tar()

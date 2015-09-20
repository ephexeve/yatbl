import argparse

# todo
class Prompt(object):
    def __init__(self):
        self.args = self.parse_arguments()

    def parse_arguments(self):
        parser = argparse.ArgumentParser(description=\
                                          "Manage the Tor browser bundle")
        
        parser.add_argument("-u", "--upgrade", help="Upgrade Tor browser to the lastest version", action="store_true")
        parser.add_argument("-r", "--uninstall", help="Uninstall the Tor browser", action="store_true")
        parser.add_argument("-i", "--install", help="Install a Tor browser version", action="store_true")
        args = parser.parse_args()
        
        return args

import os
import sys

from yatbl.downloader import Downloader
from yatbl.prompt import Prompt

def main():
    if os.getuid() == 0:
        print("Script cannot be ran as root.")
        sys.exit(1)
    
    print("Tor browser launcher")
    prompt = Prompt().args # get args
    print(prompt)
    
    if prompt.install:
        dw = Downloader()
        dw.start()
    elif prompt.uninstall: # todo, uprade tor-browser
        print("Todo - uninstall")
    elif prompt.upgrade: # todo, upgrade tor-browser
        print("Todo - upgrade")
    else: # todo, open browser
        print("Launching the browser")
        print("Bye.")

if __name__ == "__main__":
    main()

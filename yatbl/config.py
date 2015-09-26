import os

# network
tor_browser_mirror = "https://dist.torproject.org/torbrowser/{0}/"
# end network

# packages
# linux 32
tor_browser_linux32 = "tor-browser-linux32-{0}_en-US.tar.xz" # {0} = version

# linux 64
tor_browser_linux64 = "tor-browser-linux64-{0}_en-US.tar.xz" # {0} = version

# macos 64
tor_browser_macos = "TorBrowser-{0}-osx64_en-US.dmg" # {0} version
# end packages

# signing
tor_sha_file = "sha256sums-unsigned-build.txt"
tor_shasig_file = "sha256sums-unsigned-build.txt.asc"

# sys
tor_browser_location = os.path.join(os.getenv("HOME"), ".tor-browser/")
tor_browser_recommended = "https://www.torproject.org/projects/torbrowser/RecommendedTBBVersions"
file_version = "current_version"
# end sys

# gpg
tor_browser_pub_gpg = os.path.join(os.path.abspath("."), "share/torbrowser.pub")

tor_browser_path = os.path.join(os.path.abspath("$HOME"), ".tor-browser")

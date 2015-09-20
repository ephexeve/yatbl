# Yet Another Tor-browser launcher

This is still in *work in progress* status.

I decided to start this project because [torbrowser-launcher](https://github.com/micahflee/torbrowser-launcher)
has had lots of [bugs](https://bugs.debian.org/cgi-bin/pkgreport.cgi?pkg=torbrowser-launcher;dist=unstable) in the last period.
I tried looking at the their source code to see if I could help, and I noticed they are still using Python 2,
and **lots** and **lots** of external libraries. Since Debian wants to [port](https://lists.debian.org/debian-devel-announce/2015/04/msg00005.html)
everything to Python 3, I decided to create a another project written in Python 3 and try to not depend on any
external library (very hard sometimes) - currently, I am only using **python-gnupg's** external library and **python-progressbar** (optional).

## TODO's
1. Verify signatures [currently in progress].
   1. Verify sha256sum.
2. Implement browser launcher.
3. Manage different versions.
4. Add mirrors and try theses when one doesn't work.
5. Perhaps some code refactor?

### Contact
PGP fingerprint: FFBD A6F3 8BE2 E849 C46C  AD3B 7320 D3F4 FC1E E91B
Email: benmezger@riseup.net

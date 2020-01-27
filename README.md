## Cookie Extractor

Extracts all Chrome cookies found on host in a JSON file.

Cookies can then be injected using the [EditThisCookie](https://chrome.google.com/webstore/detail/editthiscookie/fngmhnnpilhplaeedifhccceomclgfbg?hl=en) Chrome extension.

Works on Windows, Linux and MacOS. 

Tested on Ubuntu 18.04 and Windows 10 (1909) with Chrome version 79.0.3945.130 (64-bit).

Made with:

* [Python](https://www.python.org/ "Python's Homepage") (3.6 or newer)

Requirements:
- [requests](https://pypi.org/project/requests/)
- [websocket-client](https://pypi.org/project/websocket_client/)

Usage:

`python cookie_extractor.py`

To compile to a single binary (e.g. executable), get [pyinstaller](https://pypi.org/project/PyInstaller/) via `pip install PyInstaller` and run:

`pyinstaller -F cookie_extractor.py`

Note that this will make the binary tied to the OS you create it on (i.e. running on Windows will create an .exe that can't run on Linux, and vice-versa).

##### Disclaimer:
Don't use this for unethical stuff!
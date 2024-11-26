# Cookie Extractor

Extracts all Chrome cookies found on host in a JSON file.

Cookies can then be injected using the [EditThisCookie](https://chromewebstore.google.com/detail/editthiscookies/hlgpnddmgbhkmilmcnejaibhmoiljhhb) Chrome extension.

Works on Windows, Linux and MacOS. 

#### Requirements:
- [Python 3.7+](https://www.python.org/downloads/)
- [requests](https://pypi.org/project/requests/)
- [websocket-client](https://pypi.org/project/websocket_client/)

#### Usage:

`python cookie_extractor.py`

#### Compile Binaries
To compile to a single binary (e.g. executable), install [pyinstaller](https://pypi.org/project/PyInstaller/) and run:

`pyinstaller --onefile cookie_extractor.py`

Note that this will make the binary tied to the OS you create it on (e.g. running on Windows will create an .exe that can't run on Linux, and vice-versa).

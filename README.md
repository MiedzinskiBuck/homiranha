# Crawler.py

[![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/release/python-360/)

Free Script to parse HTML code to find any links, enumerate directories and files.
The idea with this script is to gradually grow its functionality and enhance its performance.

Basically it is a simple tool to automate some basic Enumeration tasks.

### Install

This scrip was wrote in Python 3, so you'll need it to run the script.

```sh
$ sudo apt-get install python3
```

Clone the project or download the "crawler.py" and its pretty much good to go....at most you will have to install a python librarie...

If that happens, it is quite simple:

```sh
$ pip3 install [LIBRARIE NAME]
```

If you don't have pip3 instaled, just run:

```sh
$ sudo apt-get install pip3
```

### Usage

```sh
$ python3 crawler.py -t TARGET -w [WORDLIST] -f [FILELIST]
```

TARGET = The ULR of your target. You can just copy/paste it from your browser, the script will strip any "https://" that it needs to in case of subdomain discovery.

WORDLIST = File to use in the Directory discovery and in the Subdomain discovery. If no wordlist is specified, the script will just skip this step.

FILELIST = File to use for the file discovery. If no wordlist is specified, the script will use the wordlist in the Directory Discovery.

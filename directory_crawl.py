#!/usr/bin/python

import urllib.parse
import requests
import optparse
import re
from concurrent.futures import as_completed
from requests_futures.sessions import FuturesSession

class crawl:

    def FileCheck(wordlist):
        try:
            open(wordlist, "r")
            return 1
        except IOError:
            return 0

    def directory_discovery(target_url, wordlist):
        extension = ""
        url = target_url
        directories_list = wordlist
        if not wordlist:
            print("\033[0;33;40mSkipping directory discovery.....Use the '-w' option if you want to craw to discover directories or files....")
            pass
        else:
            print("\033[0;31;40m\n[===========================]\n\nStarting directory discovery:\n\n[===========================]\n")
            main_loop(url, directories_list, extension, discovered_directories)
            print("\033[0;34;40m\n### Searching in the discovered directories ###")
            for new_directory in discovered_directories:
                print("\033[0;34;40mEntering {0} [-]".format(new_directory))
                new_directory = new_directory[:-1]
                main_loop(new_directory, directories_list, extension, new_discovered_directories)

        for found_directory in new_discovered_directories:
            if found_directory not in discovered_directories:
                discovered_directories.append(found_directory)
        print("\033[0;34,40m\n[+] Directory searching finished with succes! [+]\n")

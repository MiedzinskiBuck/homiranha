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

    def file_discovery(target_url, wordlist, filelist):
        print("\033[0;33;40m[+]Do you want to run a file discovey?[+]\n")
        run = input("y/N:")
        run = run.lower()
        if not run or (run == "n"):
            pass
        else:
            append_list = ""
            session = FuturesSession(max_workers = 100)
            print("\033[0;31;40m\n[===========================]\n\nStarting file discovery:\n\n[===========================]\n")
            print("\033[0;33;40mWhat extension file do you want to search for?")
            extension = input("--> ")
            if not filelist:
                print("\033[0;33;40m\n[+]No File List specified, using the same wordlist: {0} [+]".format(wordlist))
                wlist = wordlist
            else:
                wlist = filelist
            print("\033[0;33;40m[+]Starting file discovery...[+]")
            main_loop(target_url, wlist, extension, append_list)
        print("\033[0;34,40m[+] File searching finished with succes! [+]")

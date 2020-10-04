#!/usr/bin/python

import urllib.parse
import requests
import optparse
import re
from concurrent.futures import as_completed
from requests_futures.sessions import FuturesSession

class crawl:

    def request(url):
        try:
            return requests.get(url)
        except requests.exceptions.ConnectionError:
            pass

    def parser(target_url):
        print("\033[0;31;40m\n[=========================]\n\nRetrieving HREF links\n\n[=========================]\n]")
        response = request(target_url)
        href_links = re.findall('(?:href=")(.*?)"', response.content.decode('utf-8'))
        for link in href_links:
            link = urllib.parse.urljoin(target_url, link)
            target_links.append(link)
            print("\033[0;32;40m{0}]".format(link))

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

    def main_loop(target_url, wordlist, extension, append_list):
        if not extension:
            extension = ""
        result = FileCheck(wordlist)
        if result == 0:
            print("\033[0;33;40m]Error: Wordlist File does not appear to exist.")
            pass
        session = FuturesSession(max_workers = 100)
        try:
            with open(wordlist, "r") as directory_file:
                futures = []
                for line in directory_file:
                    if line == "/":
                        pass
                    directory = line.strip()
                    test_directory = "{0}/{1}{2}".format(target_url, directory, extension)
                    futures.append(session.get(test_directory, timeout=5))
                for future in as_completed(futures):
                    resp = future.result()
                    if resp:
                        append_list.append(resp.url)
                        print("\033[0;32;40m[+] Discovered URL --> {0}".format(resp.url))
        except:
            print("[-] You got a time out [-]")

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

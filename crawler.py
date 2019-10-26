#!/usr/bin/python

import urllib.parse
import requests
import optparse
import re
from concurrent.futures import as_completed
from requests_futures.sessions import FuturesSession

target_links = []
discovered_directories = []
discovered_files = []
reqs = []


def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-t", "--target", dest="target", help="Specify a target URL to scan.\n\n")
    parser.add_option("-w", "--wordlist", dest="wordlist", help="Specify a wordlist to run in the directory discovery. This wordlist will be used both in the directory discover and in the subdomain discovery.\n\n")
    parser.add_option("-f", "--filelist", dest="filelist", help="Specify a wordlist to run in the file discovery. If no wordlist is specified, the file discovery will run with the same wordlist as the directory discovery.\n\n")
    (options, arguments) = parser.parse_args()

    if not options.target:
        parser.error('[-] Usage: crawler.py -t [URL] -w [WORDLIST] -f [FILELIST]')
    return options 

def request(url):
    try:
        return requests.get(url)
    except requests.exceptions.ConnectionError:
        pass

def parser(target_url):
    print("\033[0;31;40m\n[====================]\n\nRetrieving HREF links\n\n[====================]\n")
    response = request(target_url)
    href_links = re.findall('(?:href=")(.*?)"', response.content.decode('utf-8'))
    for link in href_links:
        link = urllib.parse.urljoin(target_url, link)
        target_links.append(link)
        print("\033[0;32;40m{0}".format(link))

def subdomain_discovery(target_url, wordlist):
    print("\033[0;33;40m[+]Do you want to run a subdomain discovery?[+]\n")
    run = input("y/N:")
    run = run.lower()
    if not run or (run == "n"):
        pass
    else:
        target_url = target_url.replace("http://", "")
        target_url = target_url.replace("https://", "")
        target_url = target_url.replace("www.", "")
        print("\033[0;31;40m\n[===========================]\n\nStarting Subdomain Discovery:\n\n[===========================]\n")
        session = FuturesSession(max_workers = 100)
        try:
            with open(wordlist, "r") as wordlist_file:
                futures = []
                for line in wordlist_file:
                    word = line.strip()
                    test_url = "http://{0}.{1}".format(word, target_url)
                    futures.append(session.get(test_url, timeout=5))
                for future in as_completed(futures):
                    resp = future.result()
                    if resp:
                        print("\033[0;32;40m[+] Discovered subdomain --> {0}".format(resp.url))
        except:
            print("[-] You got a time out [-]")

    print("\033[0;34;40m[+] Subdomain searching finished with success! [+]\n")

def directory_discovery(target_url, wordlist):
    url = target_url
    directories_list = wordlist
    if not wordlist:
        print("\033[0;33;40mSkipping directory discovery.....Use the '-w' option if you want to craw to discover directories or files....")
        pass
    else:
        print("\033[0;31;40m\n[===========================]\n\nStarting directory discovery:\n\n[===========================]\n")
        directory_loop(url, directories_list)
        print("\033[0;34;40m\n### Searching in the discovered directories ###")
        for new_directory in discovered_directories:
            directory_loop(new_directory, directories_list)

    print("\033[0;34,40m\n[+] Directory searching finished with succes! [+]\n")
    
def directory_loop(target_url, wordlist):
    session = FuturesSession(max_workers = 100)
    try:
        with open(wordlist, "r") as directory_file:
            futures = []
            for line in directory_file:
                directory = line.strip()
                test_directory = "{0}/{1}".format(target_url, directory)
                futures.append(session.get(test_directory, timeout=5))
            for future in as_completed(futures):
                resp = future.result()
                if resp:
                    print("\033[0;32;40m[+] Discovered URL --> {0}".format(resp.url))
    except:
        print("[-] You got a time out [-]")

def file_discovery(target_url, wordlist, filelist):
    session = FuturesSession(max_workers = 100)
    print("\033[0;33;40m[+]Do you want to run a file discovey?[+]\n")
    run = input("y/N:")
    run = run.lower()
    if not run or (run == "n"):
        pass
    else:
        print("\033[0;31;40m\n[===========================]\n\nStarting file discovery:\n\n[===========================]\n")
        print("\033[0;33;40mWhat extension file do you want to search for?")
        extension = input("--> ")
        if not filelist:
            print("\033[0;33;40m\n[+]No File List specified, using the same wordlist: {0} [+]".format(wordlist))
            wlist = wordlist
        else:
            wlist = filelist
        print("\033[0;33;40m[+]Starting file discovery...[+]")
        with open(wlist, "r") as filename_file:
            futures = []
            for line in filename_file:
                filename = line.strip()
                test_file = "{0}/{1}{2}".format(target_url, filename, extension) 
                futures.append(session.get(test_file, timeout=5))
            for future in as_completed(futures):
                file_reach = future.result()
                if file_reach:
                    print("\033[0;32;40m[+] Discovered File--> {}".format(test_file))
                    discovered_files.append(test_file)

    print("\033[0;34,40m[+] File searching finished with succes! [+]")

options = get_arguments()
wlist = options.wordlist
parser(options.target)
directory_discovery(options.target, wlist)
subdomain_discovery(options.target, wlist)
file_discovery(options.target, wlist, options.filelist)

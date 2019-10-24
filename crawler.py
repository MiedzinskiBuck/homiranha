#!/usr/bin/python

import urllib.parse
import requests
import optparse
import re

target_links = []
discovered_directories = []
discovered_files = []


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
        with open(wordlist, "r") as wordlist_file:
            for line in wordlist_file:
                word = line.strip()
                test_url = "https://{0}.{1}".format(word, target_url)
                response = request(test_url)
                if response:
                    print("\033[0;32;40m[+] Discovered subdomain --> {0}".format(test_url))

    print("\033[0;34;40m[+] Subdomain searching finished with success! [+]\n")

def directory_discovery(target_url, wordlist):
    if not wordlist:
        print("\033[0;33;40mSkipping directory discovery.....Use the '-w' option if you want to craw to discover directories or files....")
        pass
    else:
        print("\033[0;31;40m\n[===========================]\n\nStarting directory discovery:\n\n[===========================]\n")
        with open(wordlist, "r") as directory_file:
            for line in directory_file:
                directory = line.strip()
                test_directory = "{0}/{1}".format(target_url, directory)
                response = requests.get(test_directory)
                if response:
                    print("\033[0;32;40m[+] Discovered URL --> {0}".format(test_directory))
                    discovered_directories.append(test_directory)
            for new_directory in discovered_directories:
                print("\033[0;34;40m\n### Entering {0} ###\n".format(new_directory))
                with open(wordlist, "r") as new_directory_file:
                    for l in new_directory_file:
                        subdirectory = line.strip()
                        new_test_directory = new_directory + subdirectory
                        response = requests.get(new_test_directory)
                        if response:
                            print("\033[0;32;40m[+] Discovered a new URL --> {}".format(new_test_directory))
                            discovered_directories.append(new_test_directory)

    print("\033[0;34,40m\n[+] Directory searching finished with succes! [+]\n")

def file_discovery(target_url, wordlist, filelist):
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
            for line in filename_file:
                filename = line.strip()
                test_file = "{0}/{1}{2}".format(target_url, filename, extension) 
                file_reach = requests.get(test_file)
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

#!/usr/bin/python

import optparse
import directory_crawl
import file_crawl

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

def main():
    print("\033[0;31;40m\n[============================================================================]")
    print("\033[0;34;40m\nStarting HOMIRANHA!! - Remember: With great power, comes great responsability!")
    print("\033[0;31;40m\n[============================================================================]")
    options = get_arguments()

    target_links = []
    discovered_directories = []
    new_discovered_directories = []
    discovered_files = []
    reqs = []

    wlist = options.wordlist


if __name__ == "__main__":
    main()

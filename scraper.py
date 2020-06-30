#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Given at least one webpage,
search for certain price points and products availability routinely.
"""


from bs4 import BeautifulSoup
import requests
# import schedule
import time
from datetime import datetime
import logging
import argparse
import sys
import signal

__author__ = "Patrick Buzzo"


stdout_fileno = sys.stdout
logger = logging.getLogger(__file__)
url = "https://chicago.craigslist.org/d/software-qa-dba-etc/search/sof"
craigspage = requests.get(url)
logger.info('Downloading page %s...' % url)
logger.info('Checking for posts...')
craigspage.raise_for_status()
soup = BeautifulSoup(craigspage.content, 'html.parser')
exit_flag = False

keyword_list = [
    'developer',
    'PHP',
    'tech'
]


def signal_handler(sig, frame):
    """
    When SIGINT or SIGTERM is provided, this function will
    alter global exit flag variable to cause an exit
    """
    logger.info('Signal Received By Program: ' + signal.Signals(sig).name)
    global exit_flag
    if sig == signal.SIGINT or signal.SIGTERM:
        logger.info('Shutting Down Craigslist Program...')

        # Will cause termination of program, when changed to true,
        # the program terminates
        exit_flag = True


def searcher():
    with open('craigslist.txt', 'a+') as medFile:
        medFile.write(
            f"<----------- Results From: {datetime.now()} START ----------->\n\n"
        )
        liTag = soup.find_all("li", {"class": "result-row"})

        for div in liTag:
            pTags = div.find_all("p", {"class": "result-info"})
            for pars in pTags:
                aTags = pars.find_all("a", {"class": "result-title"})
                for anchor in aTags:
                    for word in keyword_list:
                        lowered = word.lower()
                        lower_anchor = anchor.text.lower()
                        if lowered in lower_anchor:
                            medFile.write("Title: " + anchor.text + "   URL: " + anchor.get('href'))
                            medFile.write('\n')
        medFile.write(
            f"\n<----------- Results From: {datetime.now()} FINISH ----------->"
        )
    line_count = 0
    lines_seen = set()     # holds lines already seen
    with open("output_file.txt", "w+") as output_file:
        for each_line in open("craigslist.txt", "r"):
            if each_line not in lines_seen:      # check if line is not duplicate
                if each_line[0] != "<":
                    if each_line[0] != "\n":
                        
                        output_file.write(each_line)
                        lines_seen.add(each_line)
    with open("output_file.txt", "r") as output_file:
        count = 0
        for line in output_file:
            count += 1
        if count == 0:
            line_count = count
        elif line_count < count:
            logger.info(f"New Found Jobs!\nCurrent Findings In Queue: {count}")
            line_count = count
        elif line_count == count:
            logger.info(f"No New Jobs Found!\nCurrent Findings In Queue: {count}")

    logger.info('Rechecking for posts...')


def create_parser():
    """
    Create parser to parse command line arguments supplied by user
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--keys', type=str, nargs="+", default="manager",
                        help='Keywords to watch for')
    parser.add_argument('--interval', type=float, default=10.0,
                        help='Number of seconds between scraping Craigslist')
    return parser


def emailer():
    """
    Create function to routinely search through
    job results and email user if new ones arefound since last check.
    """
    

def main():
    # connect logger with console output, ref Piero walkthrough
    logging.basicConfig(
        filename='dirwatcher.log',
        level=logging.DEBUG,
        format='%(asctime)s.%(msecs)03d %(name)-12s %(levelname)-8s [%(threadName)-12s] %(message)s',
        datefmt='%Y-%m--%d %H:%M:%S'
    )
    logger.setLevel(logging.DEBUG)
    # Timestamp
    app_start_time = datetime.now()
    # Start banner
    logger.info(
        '\n'
        '---------------------------------------------------------------\n'
        '    Running {0}\n'
        '    Started on {1}\n'
        '---------------------------------------------------------------\n'
        .format(__file__, app_start_time.isoformat())
    )
    # Parse command-line arguments to be used
    parser = create_parser()
    args = parser.parse_args()

    # Watch for SIGINT or SIGTERM during running of program
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    while not exit_flag:
        try:
            searcher()
        except OSError:
            logger.error('This directory does not exist')
            time.sleep(5)
        except Exception as e:
            logger.error('Unhandled exception: {}'.format(e))
        # execute watch_dirs() every [args.interval] seconds
        time.sleep(args.interval)

    # Convert uptime of program to be displayed in closing banner
    uptime = datetime.now() - app_start_time
    # Closing banner
    logger.info(
        '\n'
        '---------------------------------------------------------------\n'
        '    Stopped {0}\n'
        '    Uptime on {1}\n'
        '---------------------------------------------------------------\n'
        .format(__file__, str(uptime))
    )

if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""
Simple Web Scraper - given a URL passed in as command line argument,
returns a list of URLS, email addresses, and phone numbers included
in the page.
"""

__author__ = """Kyle Thomas, with the aid of:
             https://requests.readthedocs.io/en/master/user/quickstart/
             https://docs.python.org/3/library/re.html
             https://regex101.com/
             http://phoneregex.com/
             http://urlregex.com/
             """

import argparse
import re
import requests
import sys


def retrieve_text(url):
    """Gets the HTML from a webpage and returns it as text"""
    response = requests.get(url).text
    return response


def find_urls(text):
    """Creates a list of URLs included on a webpage"""
    url_regex = [r'http[s]?:\/\/(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|',
                 r'(?:%[0-9a-fA-F][0-9a-fA-F]))+']
    urls = re.findall(''.join(url_regex), text)
    for item in urls:
        print(item)


def find_phone_nums(text):
    """Creates a list of phone numbers included on a webpage"""
    phone_regex = [r'1?\W*([2-9][0-8][0-9])\W*([2-9][0-9]{2})',
                   r'\W*([0-9]{4})(\se?x?t?(\d*))?']
    ph_nums = (re.findall(''.join(phone_regex), text))
    for item in ph_nums:
        print(item)


def create_parser():
    """Creates an argument parser object"""
    parser = argparse.ArgumentParser()
    parser.add_argument('url', help='URL to be searched')
    return parser


def main(args):
    """Implementation of scraper.py"""
    parser = create_parser()
    ns = parser.parse_args(args)

    text = retrieve_text(ns.url)
    find_urls(text)
    find_phone_nums(text)


if __name__ == '__main__':
    main(sys.argv[1:])

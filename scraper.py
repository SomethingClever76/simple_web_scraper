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
             https://www.w3schools.com/python/python_howto_remove_duplicates.asp
             feedback from Kano Marvel
             """

import argparse
import re
import requests
import sys


def retrieve_text(url):
    """Gets the HTML from a webpage and returns it as text"""
    response = requests.get(url).text
    if '200' in response:
        return response
    else:
        return ''


def find_email(text):
    """Creates a list of email addresses included on a webpage"""
    email_regex = r'^\w+@[a-zA-Z_]+?\.[a-zA-Z]{2,3}$'
    email_addresses = (re.findall(email_regex, text))
    # filter out duplicates
    email_addresses = list(dict.fromkeys(email_addresses))
    return email_addresses


def find_phone_nums(text):
    """Creates a list of phone numbers included on a webpage"""
    phone_regex = [r'1?\W*([2-9][0-8][0-9])\W*([2-9][0-9]{2})',
                   r'\W*([0-9]{4})(\se?x?t?(\d*))?']
    ph_nums = (re.findall(''.join(phone_regex), text))
    # filter out duplicates
    ph_nums = list(dict.fromkeys(ph_nums))
    return ph_nums


def find_urls(text):
    """Creates a list of URLs included on a webpage"""
    url_regex = [r'http[s]?:\/\/(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|',
                 r'(?:%[0-9a-fA-F][0-9a-fA-F]))+']
    urls = re.findall(''.join(url_regex), text)
    # filter out duplicates
    urls = list(dict.fromkeys(urls))
    return urls


def format_result(urls, phone_nums, emails):
    print('URLS:\n')
    for item in urls:
        print(item)
    print('\nEMAILS:\n')
    if emails:
        for item in emails:
            print(item)
    else:
        print('None\n This website may be blocking' +
              'web scrapers from collecting emails')
    print('\nPHONE NUMBERS:\n')
    if phone_nums:
        for item in phone_nums:
            print(f'({item[0]}) {item[1]}-{item[2]}')
    else:
        print('None')


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
    urls = find_urls(text)
    phone_nums = find_phone_nums(text)
    emails = find_email(text)

    if text != '':
        format_result(urls, phone_nums, emails)
    else:
        print('Access was denied' +
              '\nThis website may be blocking web scrapers.')


if __name__ == '__main__':
    main(sys.argv[1:])

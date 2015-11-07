#!/usr/bin/python3

__author__ = 'andry.kondratiev@gmail.com'

import time
import whois
import string
import random
import argparse
import re


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class settings:
    domain_zone = '.com'
    domain_level = 4
    domain_symbols = 'qwertyuiopasdfghjklzxcvbnm1234567890'
    f = open('domains_found.txt', 'a')
    with open('/home/andry/programming/words') as dict_file:
        domain_dicts = dict_file.readlines()


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


parser = argparse.ArgumentParser()
parser.add_argument("-d", "--dict", action="store_true",
                    help="Find domain using dictionary")
args = parser.parse_args()
if args.dict:
    domain_to_find = settings.domain_dicts
else:
    domain_to_find = settings.domain_symbols


def dispatcher():
    while True:
        query_name=(id_generator(settings.domain_level, domain_to_find))
        try:
            domain = whois.query(query_name+settings.domain_zone)
            print(bcolors.FAIL + "Taken " + domain.name + bcolors.ENDC)
        except Exception:
            print(bcolors.OKGREEN + "FREE " + query_name + settings.domain_zone + bcolors.ENDC)
            settings.f.write(query_name + settings.domain_zone + '\n')
        time.sleep(2)




dispatcher()





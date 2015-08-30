__author__ = 'andry.kondratiev@gmail.com'

import time
import whois
import string
import random


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
    domain_zone = '.ru'
    domain_level = 2
    domain_symbols = 'qwertyuiopasdfghjklzxcvbnm123456789'
    f = open('domains_found.txt', 'a')


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def dispatcher():
    while True:
        query_name=(id_generator(settings.domain_level, settings.domain_symbols))
        try:
            domain = whois.query(query_name+settings.domain_zone)
            print(bcolors.FAIL + "Taken " + domain.name + bcolors.ENDC)
        except Exception:
            print(bcolors.OKGREEN + "FREE " + query_name + settings.domain_zone + bcolors.ENDC)
            settings.f.write(query_name + settings.domain_zone + '\n')
        time.sleep(2)

dispatcher()


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


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

domain_zone = '.ru'
domain_level = 2
domain_symbols = 'qwertyuiopasdfghjklzxcvbnm123456789'
f = open('domains_found.txt', 'a')

while True:
    query_name=(id_generator(domain_level, domain_symbols))
    try:
        domain = whois.query(query_name+domain_zone)
        print(bcolors.FAIL + "Taken " + domain.name + bcolors.ENDC)
    except Exception:
        print(bcolors.OKGREEN + "FREE " + query_name + domain_zone + bcolors.ENDC)
        f.write(query_name + domain_zone + '\n')
    time.sleep(2)


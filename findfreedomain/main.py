#!/usr/bin/env python3

import random
import string
import whois
import time
import signal
import sys

from AsyncResolver import AsyncResolver
from Settings import Settings
Settings = Settings()

__author__ = 'andry.kondratiev@gmail.com'


def signal_handler(signal, frame):
    print('You pressed Ctrl+C - exit now')
    sys.exit(0)


def generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def main():
    while True:
        query_name = (generator(Settings.domain_level, Settings.domain_symbols))
        ar = AsyncResolver([query_name+Settings.domain_zone])
        resolved = ar.resolve()
        for host, ip in resolved.items():
            signal.signal(signal.SIGINT, signal_handler)
            if ip is None:
                print("\033[92m%s could not be resolved.\033[0m" % (host))
                try:
                    domain = whois.query(host)
                    print(domain.expiration_date)
                except Exception:
                    print("\033[95mFREE " + host + "\033[0m")
                    Settings.domainsFoundFile.write(host + '\n')
                time.sleep(2)


if __name__ == '__main__':
    main()


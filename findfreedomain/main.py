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


# Функция для отлова сигнала
def signal_handler(signal, frame):
    print('You pressed Ctrl+C - exit now')
    sys.exit(0)


# Функция для генерации имени домена, вероятно добавлю словарь позже
def generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def main():
    # Бесконечный цикл
    while True:
        # Генерируем домен
        query_name = (generator(Settings.domain_level, Settings.domain_symbols))
        # Проверяем наличие домена в DNS
        ar = AsyncResolver([query_name+Settings.domain_zone])
        resolved = ar.resolve()
        # Цикл для проверки есть ли ip у домена
        for host, ip in resolved.items():
            # Ловим выход из скрипта
            signal.signal(signal.SIGINT, signal_handler)
            # Если ip нету в DNS то проверяем домен через WHOIS, сразу через WHOIS проверять нельзя
            # Так как это долго и они банят
            if ip is None:
                # Выводим информацию что ip нету в DNS
                print("\033[92m%s could not be resolved.\033[0m" % (host))
                # Обращаемся в WHOIS, если домен занят - выводим дату до которой
                # он зарегистрирован, если свободен то пишем это и записываем
                # домен в файл
                try:
                    domain = whois.query(host)
                    print(domain.expiration_date)
                except Exception:
                    print("\033[95mFREE " + host + "\033[0m")
                    Settings.domainsFoundFile.write(host + '\n')
                time.sleep(2)


if __name__ == '__main__':
    main()


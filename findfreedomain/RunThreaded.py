#!/usr/bin/env python3

import threading
from queue import Queue
import time
import random
import string
import whois
import time
import signal
import sys

from AsyncResolver import AsyncResolver
from Settings import Settings
from ConsoleColors import ConsoleColors
ConsoleColors = ConsoleColors()
Settings = Settings()

# You have exceeded allowed connection rate

print_lock = threading.Lock()

# Create the queue and threader
queue = Queue()


# Функция для отлова сигнала
def signal_handler(signal, frame):
    print('You pressed Ctrl+C - exit now')
    sys.exit(0)


# Функция для генерации имени домена, вероятно добавлю словарь позже
def generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def dispatcher(worker):
    while True:
        # Генерируем домен
        query_name = (generator(Settings.domain_level, Settings.domain_symbols))
        # Проверяем наличие домена в DNS
        ar = AsyncResolver([query_name+Settings.domain_zone])
        resolved = ar.resolve()
        # Цикл для проверки есть ли ip у домена
        for host, ip in resolved.items():
            # Если ip нету в DNS то проверяем домен через WHOIS, сразу через WHOIS проверять нельзя
            # Так как это долго и они банят
            if ip is None:
                # Выводим информацию что ip нету в DNS
                # print("\033[92m%s could not be resolved.\033[0m" % (host))
                # Обращаемся в WHOIS, если домен занят - выводим дату до которой
                # он зарегистрирован, если свободен то пишем это и записываем
                # домен в файл
                try:
                    domain = whois.query(host)
                    print("%s%s taken, expiration date %s%s" % (ConsoleColors.OKBLUE, host, domain.expiration_date, ConsoleColors.ENDC))
                except AttributeError:
                    print("%sFREE %s%s" % (ConsoleColors.OKGREEN, host, ConsoleColors.ENDC))
                    Settings.domainsFoundFile.write(host + '\n')
                except Exception:
                    print("%sERROR on %s: whois - You have exceeded allowed connection rate%s" % (ConsoleColors.FAIL, host, ConsoleColors.ENDC))
                time.sleep(2)


# The threader thread pulls an worker from the queue and processes it
def threader():
    while True:
        # gets an worker from the queue
        worker = queue.get()
        # Run the example job with the avail worker in queue (thread)
        dispatcher(worker)
        # completed with the job
        queue.task_done()


# how many threads are we going to allow for
for x in range(10):
    signal.signal(signal.SIGINT, signal_handler)
    t = threading.Thread(target=threader)
    # classifying as a daemon, so they will die when the main dies
    t.daemon = True
    # begins, must come after daemon definition
    t.start()

# 10 jobs assigned.
for worker in range(10):
    queue.put(worker)

# wait until the thread terminates.
queue.join()








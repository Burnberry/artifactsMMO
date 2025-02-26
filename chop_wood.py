import requests
from time import sleep

from helpers import *


def chop_wood():
    delay = 0
    # path = "my/Noppe/action/move"
    # data = {'x': -1, 'y': 0}
    # request = requests.post(url+path, json=data, headers=headers)
    # delay = int(request.json()['data']['cooldown']['total_seconds'])

    path = "my/Noppe/action/gathering"

    i = 0
    print(i)
    for _ in range(97):
        sleep(delay)
        i += 1
        request = requests.post(url + path, headers=headers)
        delay = int(request.json()['data']['cooldown']['total_seconds'])
        print(i, request.json())

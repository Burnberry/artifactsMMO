import requests, json
from time import sleep

import positions as p
from helpers import *
from player import Player
from characters import *

players = [Noppe(), Rubius(), Leandra(), Hella(), Pebbleboy()]
for player in players:
    player.start_thread()

input("Stop script?")

for player in players:
    player.stop_thread()

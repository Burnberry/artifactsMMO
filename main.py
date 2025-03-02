import requests, json
from time import sleep

import positions as p
from helpers import *
from player import Player
from characters import *

players = [Noppe(), Rubius(), Pebbleboy(), Leandra(), Hekate()]
for player in players[1:]:
    player.start_thread()

input("Stop script?")

for player in players:
    player.stop_thread()

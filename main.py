from characters import *

players = [Noppe(), Rubius(), Pebbleboy(), Leandra(), Hekate()]
for player in players:
    player.start_thread()

input("Stop script?")

for player in players:
    player.stop_thread()

from characters import *
from goal_script import *


players = [Noppe(), Rubius(), Pebbleboy(), Leandra(), Hekate()]

create_main_goals(players)
create_temp_goals(players)

for player in players:
    player.start_thread()

input("Stop script?")

for player in players:
    player.stop_thread()

from characters import *
from goal_script import *
from server_sync import start_sync_loop


players = [Noppe(), Rubius(), Pebbleboy(), Leandra(), Hekate()]

create_main_goals(players)
create_temp_goals(players)

sync_thread = threading.Thread(target=start_sync_loop)
sync_thread.start()

for player in players:
    player.start_thread()

input("Stop script?")

for player in players:
    player.stop_thread()
sync_thread.join()

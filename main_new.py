import threading

from player_new import Player, setup_players
from goal_script_new import *
from server_sync_new import start_sync_loop


setup_players()
create_gather_goal()
create_level_goals()
create_task_goals()
create_misc_goals()


sync_thread = threading.Thread(target=start_sync_loop)
sync_thread.start()

for player in Player.players.values():
    if player in []:
        continue
    player.start_thread()

input("")

for player in Player.players.values():
    player.stop_thread()
sync_thread.join()

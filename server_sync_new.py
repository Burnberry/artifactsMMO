from time import sleep
from helpers import *
from player_new import Player


next_syncs = []


def start_sync_loop():
    next_syncs.append((datetime.datetime.now() + datetime.timedelta(seconds=30), Player.get_active_event_data))
    _start_sync_loop()


def _start_sync_loop():
    while True:
        time, syncer = get_next_sync()
        cooldown = get_cooldown_time(time)
        if cooldown > 0:
            sleep(cooldown)

        Player.player_lock.acquire()
        syncer()
        Player.player_lock.release()

        next_syncs.append((datetime.datetime.now() + datetime.timedelta(seconds=30), syncer))


def get_next_sync():
    return next_syncs.pop()


def get_cooldown_time(time):
    now = datetime.datetime.now()
    cooldown_time = time - now
    cooldown = cooldown_time.days * 24 * 60 * 60 + cooldown_time.seconds + cooldown_time.microseconds / 10 ** 6
    return cooldown


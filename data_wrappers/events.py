from data_wrappers.data.event_data import event_data
from data_wrappers.event import Event


class Events:
    events = Event.events

    @staticmethod
    def get_event(code):
        return Events.events.get(code, None)

    portal_demon = Event(event_data['portal_demon'])
    bandit_camp = Event(event_data['bandit_camp'])
    cult_of_darkness = Event(event_data['cult_of_darkness'])
    strange_apparition = Event(event_data['strange_apparition'])
    magic_apparition = Event(event_data['magic_apparition'])
    rosenblood = Event(event_data['rosenblood'])
    portal_efreet_sultan = Event(event_data['portal_efreet_sultan'])
    cursed_tree = Event(event_data['cursed_tree'])
    fish_merchant = Event(event_data['fish_merchant'])
    timber_merchant = Event(event_data['timber_merchant'])
    herbal_merchant = Event(event_data['herbal_merchant'])
    nomadic_merchant = Event(event_data['nomadic_merchant'])
    gemstone_merchant = Event(event_data['gemstone_merchant'])

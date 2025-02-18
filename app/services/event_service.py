from typing import List
import json
from datetime import datetime


class EventService:

    def __init__(self):



        with open('events.json', 'r') as json_file:
            self.events = json.load(json_file)




    def list_events(self) -> List[str]:

        """Placeholder for list_events - to be implemented"""
        if self.events:

            events_container = []
            for event in self.events.keys():

                events_container.append(self.events[event]['Description'])

            return events_container
        else:
            raise "You have no upcoming events"









es = EventService()

print(es.list_events())
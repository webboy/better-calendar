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

                events_container.append(self.events[event]['description'])

            return events_container
        else:
            raise "You have no upcoming events"


    def add_events(self, host, location,  event_name, event_date, event_time, guests):

        try:
            date_time_str = f'{event_date} {event_time}'

            valid_date_time = datetime.strptime(date_time_str, '%d-%m-%Y %H:%M:%S')
            _date = datetime.strptime(event_date, "%d-%m-%Y")
            _time = datetime.strptime(event_time, "%H:%M:%S")
            _description = f"{event_name} on {event_date} at {event_time}"
            _event  = {}
        except ValueError:
            raise "Invalid date and time format"

        self.events[event_name] = {'name': event_name,
                                   'host': host,
                                   'location': location,
                                   'date': event_date,
                                   'time': event_time,
                                   "day_name": datetime.strftime(_date, '%A'),
                                   'is_weekday': valid_date_time.weekday() < 5 ,
                                   'month_name': datetime.strftime(_date, '%B'),
                                   'guests': guests,
                                   'description': _description}

        with open('events.json', 'w') as file:
            json.dump(self.events, file, indent=4)










es = EventService()

#print(es.list_events())
es.add_events('nem', 'zoom', "added_event", "10-10-2010", "10:10:10", ['Joud', "kehalit"])

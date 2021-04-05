import caldav
from datetime import datetime, timedelta
import re
import json
import yaml


def get_events():
    with open('config.yml') as file:
        config = yaml.load(file, Loader=yaml.FullLoader)['calendar']

    print('Fetching calendar data')
    client = caldav.DAVClient(
        url=config['url'],
        username=config['username'],
        password=config['password']
    )

    principal = client.principal()
    calendars = principal.calendars()

    events = []
    now = datetime.now()

    calendars = [c for c in calendars if c.name in config['calendars']]

    for c in calendars:
        events_fetched = c.date_search(
            start = now,
            end = now.replace(hour=23, minute=59, second=59)
        )

        for e in events_fetched:
            data = re.findall('(.+?):(.+?)\r\n', e.data)
            data_dict = {}
            for a, b in data:
                data_dict.update({a: b})

            start = datetime.strptime(data_dict['DTSTART'], '%Y%m%dT%H%M%SZ') + timedelta(hours=2)
            end = datetime.strptime(data_dict['DTEND'], '%Y%m%dT%H%M%SZ') + timedelta(hours=2)
            events.append((data_dict['SUMMARY'], start, end))

    events.sort(key=lambda tup: tup[1])

    date_format = '%H:%M'
    events = [{
        'title': a,
        'start': b.strftime(date_format),
        'end': c.strftime(date_format)
    } for a, b, c in events]

    with open('tmp/events.json', 'w') as f:
        json.dump(events, f)
        print('Calendar updated')


if __name__ == '__main__':
    get_events()

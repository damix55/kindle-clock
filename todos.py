import json
import yaml

from todoist.api import TodoistAPI
from datetime import datetime
from dateutil import tz


def get_todos():
    with open('config.yml') as file:
        token = yaml.load(file, Loader=yaml.FullLoader)['todoist']['token']

    api = TodoistAPI(token)
    api.sync()

    now = datetime.now()
    timezone = tz.gettz(api.state['user']['tz_info']['timezone'])

    todos = []

    for item in api.state['items']:
        due = item['due']
        if due is not None:
            due_date = datetime.strptime(due['date'], '%Y-%m-%d')

            if item['checked'] == 1:
                date_completed = datetime.strptime(item['date_completed'], '%Y-%m-%dT%H:%M:%S%z').astimezone(tz=timezone)
                if date_completed.date() != now.date():
                    continue

            if due_date <= now:
                todos.append({
                    'title': item['content'],
                    'priority': item['priority'],
                    'due_date': due_date,
                    'completed': item['checked']
                })

    todos = sorted(todos, key = lambda i: (i['completed'], i['due_date'], 1/i['priority']))

    tasks_dump = []

    for todo in todos:
        tasks_dump.append({
            'title': todo['title'],
            'completed': todo['completed']==1
        })

    with open('tmp/todos.json', 'w') as f:
        json.dump(tasks_dump, f)
        print('Todos updated')


if __name__ == '__main__':
    get_todos()
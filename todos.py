import yaml
import json

from ticktick import api
from datetime import datetime, timedelta


def get_todos():
    with open('config.yml') as file:
        config = yaml.load(file, Loader=yaml.FullLoader)['ticktick']

    client = api.TickTickClient(config['username'], config['password'])

    tasks_todo = client.task.get_from_project(client.inbox_id)
    tasks_completed = client.task.get_completed(datetime.now())

    temp_todo = []

    for task in tasks_todo:
        due_date = datetime.strptime(task['dueDate'][:10], '%Y-%m-%d') + timedelta(days=1)

        if due_date<=datetime.now():
            temp_todo.append({
                'title': task['title'],
                'priority': task['priority'],
                'due_date': due_date
            })

    temp_todo = sorted(temp_todo, key = lambda i: (i['due_date'], 1/i['priority']))

    tasks = [{'title':d['title'], 'completed': False} for d in temp_todo]

    for task in tasks_completed:
        tasks.append({
            'title': task['title'],
            'completed': True
        })

    with open('tmp/todos.json', 'w') as f:
        json.dump(tasks, f)
        print('Todos updated')


if __name__ == '__main__':
    get_todos()
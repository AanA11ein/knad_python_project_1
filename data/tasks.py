import datetime
from data.utils import read_data, find_user_from_data, write_data, find_task_by_id
import uuid

def create_task(text: str):
    return {
        'id': int(str(uuid.uuid1().int)[:10]),
        'text': text,
        'done': False,
        'created_at': datetime.datetime.now(datetime.UTC).isoformat(),
    }

def add_task(user_id: int, text: str):
    index, user = find_user_from_data(user_id)
    if user:
        task = create_task(text)
        user['tasks'].append(task)
        data = read_data()
        data[index] = user
        write_data(data)
        return task['id']
    return None

def mark_done(user_id: int, task_id: int):
    user_idx, user = find_user_from_data(user_id)
    task_data = find_task_by_id(user, task_id)
    if task_data:
        task_idx, task = task_data
        if task['done']:
            return False
        user['tasks'][task_idx]['done'] = True
        data = read_data()
        data[user_idx] = user
        write_data(data)
        return True
    return False

def count_tasks(user_id: int):
    _, user = find_user_from_data(user_id)
    return len(user['tasks'])

def list_tasks(user_id: int, offset: int, limit: int):
    _, user = find_user_from_data(user_id)
    tasks = user['tasks']
    return tasks[offset: offset + limit]
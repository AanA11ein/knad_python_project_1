import json
import os

from shared.file import readable_size

file_path = './data/data.json'

def read_data():
    data = []
    with open(file_path, mode='r', encoding='utf-8') as file:
        data = json.loads(file.read())
    return data

def write_data(data):
    with open(file_path, mode='w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)

def get_data_size():
    file_size_bytes = os.path.getsize(file_path)
    return readable_size(file_size_bytes)

def find_user_from_data(user_id: int):
    data = read_data()
    for i in range(len(data)):
        if data[i]['user_id'] == user_id:
            return i, data[i]
    return None

def find_task_by_id(user, task_id):
    for i in range(len(user['tasks'])):
        if user['tasks'][i]['id'] == task_id:
            return i, user['tasks'][i]
    return None
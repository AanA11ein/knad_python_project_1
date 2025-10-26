import datetime
from collections import defaultdict

from consts.commands import COMMANDS
from data.utils import read_data, get_data_size

def get_unique_users_count():
    return len(read_data())

def get_unique_commands_count():
    data = read_data()

    commands_data = defaultdict(int)

    for user in data:
        command_counts = user['command_counts']
        commands_data['command_start'] += command_counts['command_start']
        commands_data['command_help'] += command_counts['command_help']
        commands_data['command_weather'] += command_counts['command_weather']
        commands_data['command_rate'] += command_counts['command_rate']
        commands_data['command_todo'] += command_counts['command_todo']
        commands_data['command_fileinfo'] += command_counts['command_fileinfo']
        commands_data['command_stats'] += command_counts['command_stats']

    res = {}

    for command in commands_data:
        res[COMMANDS[command]] = commands_data[command]

    return res

def normalize_stats(start_time):
    uptime = datetime.datetime.now(datetime.UTC) - start_time
    unique_commands_count = get_unique_commands_count()

    return f'Uptime: {str(uptime).split('.')[0]}\nUnique users count: {get_unique_users_count()}\nData size: {get_data_size()}\nCommands count:\n{'\n'.join([f'- {k}: {v}' for k, v in unique_commands_count.items()])}'
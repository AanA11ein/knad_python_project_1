from data.utils import read_data, write_data

def create_user(user_id: int):
    return {
        'user_id': user_id,
        'tasks': [],
        'command_counts': {
            'command_start': 0,
            'command_help': 0,
            'command_weather': 0,
            'command_todo': 0,
            'command_rate': 0,
            'command_fileinfo': 0,
            'command_stats': 0,
        }
    }

def register_user(user_id: int) -> None:
    data = read_data()

    is_not_registered = len([user for user in data if user.get('user_id') == user_id]) == 0

    if is_not_registered:
        data.append(create_user(user_id))
        write_data(data)

def incr_user_command(user_id: int, command: str) -> None:
    data = read_data()

    for user in data:
        if user.get("user_id") == user_id:
            user['command_counts'][command] += 1

    write_data(data)

def handle_user(user_id: int, command: str) -> None:
    register_user(user_id)
    incr_user_command(user_id, command)


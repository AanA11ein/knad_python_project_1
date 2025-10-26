import asyncio
import datetime
import os

from aiogram.filters import CommandStart, Command
from aiogram.types import CallbackQuery
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher

from data.tasks import add_task, mark_done
from data.users import handle_user
from features.currency import fetch_currency, normalize_currency
from features.file import download_and_hash
from features.stats import normalize_stats
from features.todo import send_todo_page
from features.weather import fetch_weather, normalize_weather
from shared.file import readable_size

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

BOT_TOKEN = os.getenv('BOT_TOKEN')
WEATHER_RETRIES = os.getenv('WEATHER_RETRIES')
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')
CURRENCY_API_KEY = os.getenv('CURRENCY_API_KEY')

if not BOT_TOKEN:
    raise ValueError('BOT_TOKEN must be set')

dp = Dispatcher()
bot = Bot(token=BOT_TOKEN)

start_time = datetime.datetime.now(datetime.UTC)

@dp.message(CommandStart())
async def start_handler(message):
    handle_user(message.from_user.id, 'command_start')
    await message.answer(f'Hello, {message.from_user.username}! Please, use me! Try /help ;)')

@dp.message(Command(commands=['help']))
async def help_handler(message):
    handle_user(message.from_user.id, 'command_help')
    await message.answer(
        'Available commands:\n\n'
        '- /weather <city> — current weather by city\n'
        '- /rate <BASE> <EUR,RUB,...> — currency\n'
        '- /fileinfo — send any file\n'
        '- /stats — get statistics\n'
        '- /todo add <text> / list / done <task_id> — todo'
    )

@dp.message(Command(commands=['weather']))
async def weather_handler(message):
    handle_user(message.from_user.id, 'command_weather')
    city = message.text.strip()[8:].strip()
    if not city:
        await message.reply('Please specify a city')
        return
    data = await fetch_weather(city, int(WEATHER_RETRIES), WEATHER_API_KEY)
    if type(data) is str:
        await message.reply(data)
    else:
        await message.reply(normalize_weather(city, data))

@dp.message(Command(commands=['rate']))
async def rate_handler(message):
    handle_user(message.from_user.id, 'command_rate')
    data = message.text.strip().split()
    if len(data) < 3:
        await message.reply('Please specify currency')
        return
    base = data[1]
    syms = data[2]
    res = await fetch_currency(base, CURRENCY_API_KEY)
    if type(res) is str:
        await message.reply(res)
    else:
        await message.reply(normalize_currency(res, base, syms))

@dp.message(Command(commands=['fileinfo']))
async def fileinfo_handler(message):
    handle_user(message.from_user.id, 'command_fileinfo')
    if message.document:
        file_id = message.document.file_id
        filename = message.document.file_name
    elif message.photo:
        photo = message.photo[-1]
        file_id = photo.file_id
        filename = 'photo.jpg'
    elif message.video:
        file_id = message.video.file_id
        filename = getattr(message.video, 'file_name', 'video.mp4')
    elif message.audio:
        file_id = message.audio.file_id
        filename = getattr(message.audio, 'file_name', 'audio.mp3')
    elif message.voice:
        file_id = message.voice.file_id
        filename = 'voice.ogg'
    else:
        await message.reply('Please, send file with command (document/photo/video/audio/voice).')
        return

    file = await bot.get_file(file_id)
    sha256, size = await download_and_hash(file.file_path, BOT_TOKEN)

    await message.reply(
        f'Filename: {filename}\n'
        f'Size: {size} bite ({readable_size(size)})\n'
        f'SHA-256: {sha256}'
    )

@dp.message(Command(commands=['stats']))
async def stats_handler(message):
    handle_user(message.from_user.id, 'command_stats')
    await message.reply(normalize_stats(start_time))

@dp.message(Command(commands=['todo']))
async def todo_handler(message, command):
    handle_user(message.from_user.id, 'command_todo')

    args = command.args
    if not args:
        await message.reply('Subcommands todo: add <text>, list, done <task_id>')
        return

    parts = args.split(maxsplit=1)
    sub = parts[0].lower()

    match sub:
        case 'add':
            if len(parts) < 2 or not parts[1].strip():
                await message.reply('Specify the text of the todo')
                return
            text = parts[1].strip()
            task_id = add_task(message.from_user.id, text)
            await message.reply(f'Added.\n\nTask: {text}\nTask ID: {task_id}')
        case 'done':
            if len(parts) < 2 or not parts[1].strip():
                await message.reply('Specify the ID of the todo')
                return
            try:
                task_id = int(parts[1].strip())
            except Exception:
                await message.reply('Invalid task ID')
                return
            ok = mark_done(message.from_user.id, task_id)
            if ok:
                await message.reply(f'Task ID {task_id} is marked as done.')
            else:
                await message.reply(f"Couldn't mark the task #{task_id}, maybe it doesn't exist or it's already done")
        case 'list':
            page = 1
            await send_todo_page(message, message.from_user.id, page)
        case _:
            await message.reply('Invalid subcommands, try: add <text>, list, done <task_id>')

@dp.callback_query(lambda c: c.data and c.data.startswith('todo_page:'))
async def cb_todo_page(cb: CallbackQuery):
    handle_user(cb.from_user.id, 'command_todo')
    try:
        _, user_id, page = cb.data.split(":")
        user_id = int(user_id)
        page = int(page)
    except Exception:
        await cb.answer('Incorrect navigation data.')
        return
    if cb.from_user.id != user_id:
        await cb.answer('This is not your todo list')
        return
    await send_todo_page(cb, user_id, page, edit=True, cb_query=cb)

async def main() -> None:
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())

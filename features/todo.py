from aiogram.types import InlineKeyboardMarkup, CallbackQuery, InlineKeyboardButton, Message

from data.tasks import count_tasks, list_tasks

async def send_todo_page(message_or_cb, user_id: int, page: int = 1, edit: bool = False, cb_query: CallbackQuery | None = None):
    per_page = 10
    total = count_tasks(user_id)
    max_page = max(1, (total + per_page - 1) // per_page)
    if page < 1:
        page = 1
    if page > max_page:
        page = max_page
    offset = (page - 1) * per_page
    tasks = list_tasks(user_id, offset, per_page)
    if not len(tasks):
        text = 'Todo list empty.' if total == 0 else 'No tasks found.'
    else:
        lines = []
        for task in tasks:
            status = '✅' if task['done'] else '❌'
            lines.append(f"{status} {task['text']} (ID: {task['id']})")
        text = '\n'.join(lines)
    text = f'Tasks (page {page}/{max_page}, total: {total}):\n\n' + text

    kb = InlineKeyboardMarkup(row_width=2, inline_keyboard=[])
    if page == 1 and max_page != 1:
        kb.inline_keyboard = [[InlineKeyboardButton(text='Forward ➡️', callback_data=f'todo_page:{user_id}:{page + 1}')]]
    elif page == max_page and page != 1:
        kb.inline_keyboard = [[InlineKeyboardButton(text='⬅️ Backward', callback_data=f'todo_page:{user_id}:{page - 1}')]]
    elif not (page == 1 and max_page == 1):
        kb.inline_keyboard = [[InlineKeyboardButton(text='⬅️ Backward', callback_data=f'todo_page:{user_id}:{page - 1}')],[InlineKeyboardButton(text='Forward ➡️', callback_data=f'todo_page:{user_id}:{page + 1}')]]

    if edit and cb_query is not None:
        try:
            await cb_query.message.edit_text(text)
            await cb_query.message.edit_reply_markup(reply_markup=kb)
            await cb_query.answer()
        except Exception:
            await cb_query.answer()
    else:
        if isinstance(message_or_cb, Message):
            await message_or_cb.answer(text, reply_markup=kb)
        else:
            await message_or_cb.reply(text, reply_markup=kb)

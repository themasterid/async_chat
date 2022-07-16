import asyncio

from pywebio import start_server
from pywebio.input import *
from pywebio.output import (output, put_buttons, put_markdown, put_scrollable,
                            toast)
from pywebio.session import run_async, run_js

chat_msg = []
online_users = set()

MAX_MESSAGES_COUNT = 100


async def main():
    global chat_msg
    put_markdown('ИСУ Контроль')

    msg_box = output()
    put_scrollable(msg_box, height=400, keep_bottom=True)

    nickname = await input(
        '',
        required=True,
        placeholder='Придумай себе никнейм...',
        validate=lambda n: (
            'Такой никнейм уже используется!'
            if n in online_users or n == 'X'
            else None))
    online_users.add(nickname)

    chat_msg.append((f'`{nickname}` присоединился!'))
    msg_box.append(put_markdown(f'`{nickname}` в чате.'))

    refresh_task = run_async(refresh_msg(nickname, msg_box))

    while True:
        data = await input_group('', [
            input(placeholder='Сюда пишем текст сообщения....', name='msg'),
            actions(
                name='cmd',
                buttons=[
                    'Отправить',
                    {
                        'label': 'Выйти из чата',
                        'type': 'cancel'}])
        ], validate=lambda m: (
            'msg',
            'Нужно что-то написать :)')
            if m['cmd'] == 'Отправить' and not m['msg']
            else None)

        if data is None:
            break
        msg_box.append(put_markdown(f'`{nickname}`: {data["msg"]}'))
        chat_msg.append((nickname, data['msg']))
    refresh_task.close()
    online_users.remove(nickname)
    toast('До новых встреч!')
    msg_box.append(put_markdown(f'`{nickname}` вышел.'))
    chat_msg.append((f'{nickname}` вышел.'))

    put_buttons(
        ['Вернутся в чат'],
        onclick=lambda btn:run_js('window.location.reload()'))


async def refresh_msg(nickname: str, msg_box: str):
    global chat_msg
    last_idx = len(chat_msg)
    while True:
        await asyncio.sleep(1)
        for m in chat_msg[last_idx:]:
            if m[0] != nickname:
                msg_box.append(put_markdown(f'`{m[0]}`: {m[1]}'))
        if len(chat_msg) > MAX_MESSAGES_COUNT:
            chat_msg = chat_msg[len(chat_msg) // 2:]
        last_idx = len(chat_msg)


if __name__ == '__main__':
    start_server(
        main,
        debug=True,
        port=8080,
        cdn=False)

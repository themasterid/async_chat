import asyncio
import time
from typing import Set

from pywebio import start_server
from pywebio.input import input, input_group, actions, validate
from pywebio.output import output, put_markdown, put_scrollable, put_buttons, toast
from pywebio.session import run_async

chat_messages: list[tuple[str, str]] = []
online_users: Set[str] = set()
last_rendered_index: int = 0

async def validate_nickname(nickname: str) -> None:
    if nickname in online_users or nickname == '':
        raise ValueError("Такой никнейм уже используется!")

async def validate_message(msg: str) -> None:
    if not msg.strip():
        raise ValueError("Нужно что-то написать :)")

async def refresh_ui(nickname: str, msg_container):
    global chat_messages, last_rendered_index, MAX_MESSAGES_COUNT
    
    try:
        while True:
            await asyncio.sleep(1.0)
            
            for msg_idx in range(last_rendered_index, len(chat_messages)):
                user_name, msg_text = chat_messages[msg_idx]
                
                if user_name != nickname:
                    msg_container.append(put_markdown(f'**{user_name}**: {msg_text}'))
            
            if len(chat_messages) > MAX_MESSAGES_COUNT:
                chat_messages = chat_messages[MAX_MESSAGES_COUNT - MAX_MESSAGES_COUNT // 2:]
                last_rendered_index = MAX_MESSAGES_COUNT // 2
    except asyncio.CancelledError:
        pass

async def main():
    global chat_messages, online_users, last_rendered_index, msg_container
    
    chat_messages = []
    online_users = set()
    last_rendered_index = 0

    msg_container = output()
    put_scrollable(msg_container, height=400, keep_bottom=True)
    msg_container.append(put_markdown('ИСУ Контроль'))
    
    nickname = await input(
        '',
        required=True,
        placeholder='Придумай себе никнейм...',
        validate=validate_nickname
    )
    
    online_users.add(nickname)
    chat_messages.append((f'{nickname} присоединился!'))
    msg_container.append(put_markdown(f'**{nickname}** в чате.'))

    refresh_task = run_async(refresh_ui, nickname, msg_container)
    
    try:
        while True:
            data = await input_group('', [
                input(
                    placeholder='Сюда пишем текст сообщения....',
                    name='msg',
                    validate=validate_message
                ),
                actions(
                    name='cmd',
                    buttons=[
                        'Отправить',
                        {
                            'label': 'Выйти из чата',
                            'type': 'cancel'
                        }
                    ]
                )
            ])
            
            if data is None:
                break
            
            if data['cmd'] == 'Отправить':
                text = data['msg']
                chat_messages.append((nickname, text))
                msg_container.append(put_markdown(f'**{nickname}**: {text}'))
                
    except Exception as e:
        print(f"Chat Error: {e}")
    finally:
        if 'refresh_task' in locals():
            refresh_task.close()
            
        online_users.discard(nickname)
        
        msg_container.append(put_markdown(f'**{nickname}** ушел.'))
        toast('До новых встреч!')

    put_buttons(
        ['Вернуться в чат'],
        onclick=lambda btn: run_js('window.location.reload()')
    )

if __name__ == '__main__':
    start_server(
        main,
        debug=True,
        port=8080,
        cdn=False
    )

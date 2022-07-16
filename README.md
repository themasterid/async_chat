# async_chat - чат который можно встроить в любой проект на базе ЯП Python.

Async чат на ваш сервис - простой чат, который будет с доработками работать вам долго и интересно.

## Установка

Все что нужно, клонируем или форкаем:

```bash
git clone git@github.com:themasterid/async_chat.git
```

Переходим в репозиторий:

```bash
cd async_chat
```

Создаем виртуальное окружение (ВО):

```bash
python -m venv venv
```

Активируем его (ВО) с обновлением pip:

```bash
source /venv/bin/activate # linux
source /venv/Scripts/activate # windows
python -m pip install --upgrade pip
```

Устанавливаем зависимости:

```bash
pip install -r requirements.txt
```

И запускаем чат:

```bash
python chat.py
```

Изучаем работу чата, и интегрируем в любую систему на ваш вкус.

Автор: [Клепиков Дмитрий](https://github.com/themasterid)
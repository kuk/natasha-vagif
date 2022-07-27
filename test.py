
from json import (
    loads as parse_json,
    dumps as format_json
)

from aiogram.types import Update

from main import (
    Bot,
    Dispatcher,
    setup_handlers
)


class FakeBot(Bot):
    def __init__(self):
        Bot.__init__(self, token='123:faketoken')
        self.trace = []

    async def request(self, method, data):
        json = format_json(data, ensure_ascii=False)
        self.trace.append([method, json])
        return {}


async def process_update(json):
    data = parse_json(json)
    update = Update(**data)

    bot = FakeBot()
    dispatcher = Dispatcher(bot)

    # To access bot implicitly in message.delete. Mock set_current in
    # start_polling
    Bot.set_current(bot)
    Dispatcher.set_current(dispatcher)

    setup_handlers(dispatcher)

    await dispatcher.process_update(update)
    return bot.trace


async def test_new_member():
    json = '{"update_id": 836538909, "message": {"message_id": 3, "from": {"id": 113947584, "is_bot": false, "first_name": "Alexander", "last_name": "Kukushkin", "username": "alexkuk", "language_code": "ru"}, "chat": {"id": -1001721390626, "title": "vagif_bot_test_chat", "username": "vagif_bot_test_chat", "type": "supergroup"}, "date": 1657200024, "new_chat_participant": {"id": 113947584, "is_bot": false, "first_name": "Alexander", "last_name": "Kukushkin", "username": "alexkuk", "language_code": "ru"}, "new_chat_member": {"id": 113947584, "is_bot": false, "first_name": "Alexander", "last_name": "Kukushkin", "username": "alexkuk", "language_code": "ru"}, "new_chat_members": [{"id": 113947584, "is_bot": false, "first_name": "Alexander", "last_name": "Kukushkin", "username": "alexkuk", "language_code": "ru"}]}}'
    trace = await process_update(json)
    assert trace == [['deleteMessage', '{"chat_id": -1001721390626, "message_id": 3}']]


async def test_left_member():
    json = '{"update_id": 836538908, "message": {"message_id": 2, "from": {"id": 113947584, "is_bot": false, "first_name": "Alexander", "last_name": "Kukushkin", "username": "alexkuk", "language_code": "ru"}, "chat": {"id": -1001721390626, "title": "vagif_bot_test_chat", "username": "vagif_bot_test_chat", "type": "supergroup"}, "date": 1657199623, "left_chat_participant": {"id": 113947584, "is_bot": false, "first_name": "Alexander", "last_name": "Kukushkin", "username": "alexkuk", "language_code": "ru"}, "left_chat_member": {"id": 113947584, "is_bot": false, "first_name": "Alexander", "last_name": "Kukushkin", "username": "alexkuk", "language_code": "ru"}}}'
    trace = await process_update(json)
    assert trace == [['deleteMessage', '{"chat_id": -1001721390626, "message_id": 2}']]


async def test_message():
    json = '{"update_id": 836538902, "message": {"message_id": 10, "from": {"id": 5428138451, "is_bot": false, "first_name": "Alexander", "last_name": "Kukushkin", "language_code": "ru"}, "chat": {"id": 5428138451, "first_name": "Alexander", "last_name": "Kukushkin", "type": "private"}, "date": 1657195845, "text": "/start", "entities": [{"offset": 0, "length": 6, "type": "bot_command"}]}}'
    trace = await process_update(json)
    assert trace == []

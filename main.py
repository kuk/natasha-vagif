
from os import getenv

from aiogram import (
    Bot,
    Dispatcher
)
from aiogram.types import ContentType
from aiogram.utils.executor import start_webhook


BOT_TOKEN = getenv('BOT_TOKEN')
PORT = getenv('PORT', 8080)


async def delete_message(message):
    await message.delete()


def setup_handlers(dispatcher):
    dispatcher.register_message_handler(
        delete_message,
        content_types=(
            ContentType.NEW_CHAT_MEMBERS,
            ContentType.LEFT_CHAT_MEMBER
        )
    )


if __name__ == '__main__':
    bot = Bot(token=BOT_TOKEN)
    dispatcher = Dispatcher(bot)
    setup_handlers(dispatcher)

    start_webhook(
        dispatcher=dispatcher,
        webhook_path='/',
        port=PORT
    )

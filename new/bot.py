import asyncio
#from handlers import router
from aiogram import Bot, Dispatcher, BaseMiddleware
from typing import Any, Awaitable, Callable, Dict, List, Union
import hd_admin
import resender_hd
from aiogram.types import (
    Message,
    TelegramObject,
)
from user_data import ADMIN_ID, TOKEN, db_path
from database import DbSpamer
import os



DEFAULT_DELAY = 1.3



class MediaGroupMiddleware(BaseMiddleware):
    ALBUM_DATA: Dict[str, List[Message]] = {}

    def __init__(self, delay: Union[int, float] = DEFAULT_DELAY):
        self.delay = delay

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        if not event.media_group_id:
            return await handler(event, data)

        try:
            self.ALBUM_DATA[event.media_group_id].append(event)
            return
        except KeyError:
            self.ALBUM_DATA[event.media_group_id] = [event]
            await asyncio.sleep(self.delay)
            data["album"] = self.ALBUM_DATA.pop(event.media_group_id)

        return await handler(event, data)


async def on_bot_startup(bot: Bot):
    await bot.send_message(chat_id=ADMIN_ID , text="Bot started!")


async def on_bot_shutdown(bot: Bot):
    await bot.send_message(chat_id=ADMIN_ID, text="Bot shutdown!")


async def on_startup(bots: List[Bot]):
    for bot in bots:
        await on_bot_startup(bot)


async def on_shutdown(bots: List[Bot]):
    for bot in bots:
        await on_bot_shutdown(bot)


async def main():

    if not os.path.exists(db_path):
        with DbSpamer() as db:
            db.db_check_and_create_tables()

    bot = Bot(TOKEN)
    dp = Dispatcher()

    dp.startup.register(on_startup) 
    dp.shutdown.register(on_shutdown)

    dp.include_routers(hd_admin.router)
    dp.include_routers(resender_hd.router)
    dp.message.middleware(MediaGroupMiddleware())

    await bot.get_updates(offset=-1)
    await dp.start_polling(bot)



if __name__ == "__main__":
    asyncio.run(main())

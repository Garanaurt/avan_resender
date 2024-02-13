from telethon.sync import TelegramClient, events
import asyncio
from user_data import API_HASH, API_ID, API_NUM, USERNAME



api_id = API_ID
api_hash = API_HASH
phone_number = API_NUM
bot_username = USERNAME



client = TelegramClient(phone_number, api_id, api_hash)

confirmation_code = ''

async def main():
    await client.start(phone_number)

    @client.on(events.Album)
    async def album_handler(event):
        await event.forward_to(bot_username)


    @client.on(events.NewMessage)
    async def message_handler(event: events.NewMessage.Event):
        if event.message.grouped_id:
            return
        await client.forward_messages(bot_username, event.message)

    await client.run_until_disconnected()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
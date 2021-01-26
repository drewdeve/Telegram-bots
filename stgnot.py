import logging
import asyncio
from datetime import datetime

from aiogram import Bot, types
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher
from sqlighterforst import SQLighter
from stopgame import StopGame

logging.basicConfig(format=u'%(filename)+13s [ LINE:%(lineno)-4s] %(levelname)-8s [%(asctime)s] %(message)s',
                    level=logging.INFO)

bot = Bot(token='1319711015:AAHeU7JPtIxljW4MXmfHdxhlYQJ5ADx_naI')
dp = Dispatcher(bot)

db = SQLighter('C:/telegram-bot/dbforstgnot.db')

sg = StopGame('C:/telegram-bot/lastkey.txt')

@dp.message_handler(commands=['subscribe'])
async def subscribe(message: types.Message):
    if(not db.subscriber_exists(message.from_user.id)):
        db.add_subscriber(message.from_user.id)
    else: 
        db.update_subscription(message.from_user.id, True)

    await message.answer("You have successfully subscribed to the newsletter!\nWait, new reviews will come out soon  and you will be the first to know about them =)")

@dp.message_handler(commands=['unsubscribe'])
async def unsubscribe(message: types.Message):
    if (not db.subscriber_exists(message.from_user.id)):
        db.add_subscriber(message.from_user.id, False)
        await message.answer("You're not subscribe.")
    else:
        db.update_subscription(message.from_user.id, False)
        await message.answer("You have successfully been discharged from the mailing list.")

async def scheduled(wait_for):
    while True:
        await asyncio.sleep(wait_for)

        new_games = sg.new_games()

        if(new_games):
            new_games.reverse()
            for ng in new_games:
                nfo = sg.game_info(ng)
                subscriptions = db.get_subscriptions()
                with open(sg.download_image(nfo['image']), 'rb') as photo:
                    for s in subscriptions:
                        await bot.send_photo(
                            s[1],
                            photo,
                            caption = nfo['title'] + "\n" + "Score: " + nfo['score'] + "\n" + nfo['excerpt'] + "\n\n" + nfo['link'],
                            disable_notification = True
                        )
                sg.update_lastkey(nfo['id'])

if __name__ == '__main__':
    dp.loop.create_task(scheduled(10))
    executor.start_polling(dp, skip_updates=True)
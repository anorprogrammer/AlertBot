from datetime import datetime, timedelta

import logging

from aiogram import Bot, Dispatcher, executor, types
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from config import BOT_TOKEN

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)
scheduler = AsyncIOScheduler(timezone='Asia/Tashkent')


async def send_alert(chat_id, text):
    await bot.send_message(chat_id, text)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    text = """
    Use this format to create alerts:
/alert time text
'Text' is anything you want the bot to tell you.
    """
    await message.answer(text)


@dp.message_handler(commands=['time'])
async def time(message: types.Message):
    full_command = message.get_full_command()
    context = full_command[1].split()
    minute = context[0]
    text = ' '.join(context[1:])

    alert_time = datetime.now() + timedelta(minutes=int(minute))

    schedule_alert(message.chat.id, text, alert_time)
    await message.answer(f'Alert time: {alert_time}')


def schedule_alert(chat_id, text, alert_time):
    scheduler.add_job(send_alert, 'date', run_date=alert_time, args=[chat_id, text])


if __name__ == '__main__':
    scheduler.start()
    executor.start_polling(dp, skip_updates=True)

import asyncio
import json
import logging
import sys
from aiogram import Bot, Dispatcher, types
from config import bot_token
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

logging.basicConfig(level=logging.INFO)
bot = Bot(token=bot_token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
    await message.answer("Привет!")


@dp.message_handler(commands=["web"])
async def cmd_web(message: types.Message):
    keyboard = InlineKeyboardMarkup().add(
        InlineKeyboardButton("Open Web", web_app=types.WebAppInfo(url="https://samakonalocal.ru")),
    )
    await bot.send_message(chat_id=message.chat.id,
                           text="Да пожалуйста:",
                           reply_markup=keyboard)


# Под рассылку
@dp.message_handler(commands=['sendall'])
async def send_all(message: types.Message):
    admin_id = 1643016272
    if message.chat.id == 1643016272:
        await message.answer("Старт")
        users = []
        for i in users:
            await bot.send_message(chat_id=i, text="Текст")
        await message.answer('Рассылка окончена')
    else:
        await message.answer('Ошибка авторизации')


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    executor.start_polling(dp, skip_updates=True)
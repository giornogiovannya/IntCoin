import asyncio
import json
import logging
import sys
from aiogram import Bot, Dispatcher, types
from config import goods_bot_token
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

logging.basicConfig(level=logging.INFO)
bot = Bot(token=goods_bot_token)
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


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    executor.start_polling(dp, skip_updates=True)
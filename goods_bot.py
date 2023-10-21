import asyncio
import json
import logging
import sys
from aiogram import Bot, Dispatcher, types
from config import goods_bot_token
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputFile
from db import goods_get_nickname, goods_get_avatar, goods_get_intcoins, goods_get_last_trades, goods_new_user_first_time

logging.basicConfig(level=logging.INFO)
bot = Bot(token=goods_bot_token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
PHOTO_SERVER_PATH = ""


@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
    goods_new_user_first_time(message.from_user.id, message.from_user.first_name)
    await message.answer("Привет!")


@dp.message_handler(commands=["web"])
async def cmd_web(message: types.Message):
    keyboard = InlineKeyboardMarkup().add(
        InlineKeyboardButton("Открыть Магазин Ништяков", web_app=types.WebAppInfo(url="https://samakonalocal.ru")),
    )
    await bot.send_message(chat_id=message.chat.id,
                           text="Магазин по кнопочке ниже:",
                           reply_markup=keyboard)


@dp.message_handler(commands=["status"])
async def cmd_status(message: types.Message):
    # Получаем из бд аватар, никнейм, последние 10 переводов
    # Формируем ответ
    user_id = message.from_user.id
    user_nickname = goods_get_nickname(user_id)
    user_avatar = goods_get_avatar(user_id)
    user_avatar_file = InputFile(user_avatar)
    user_intcoins = goods_get_intcoins(user_id)
    user_last_trades = goods_get_last_trades(user_id)

    caption = f"{user_nickname}\n\nБаланс Инткоинов: {user_intcoins}\n\n{user_last_trades}"
    await message.answer_photo(photo=user_avatar_file, caption=caption)


@dp.message_handler(commands=["help"])
async def cmd_help(message: types.Message):
    await message.answer("/status - Получить краткую информацию об аккаунте\n/setavatar - Установить аватарку\n/setnickname - Установить никнейм\n/web - Открыть Магазин Ништяков, если кнопка меню недоступна\n")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    executor.start_polling(dp, skip_updates=True)
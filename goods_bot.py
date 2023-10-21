import asyncio
import json
import logging
import sys
from aiogram import Bot, Dispatcher, types
from config import goods_bot_token
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputFile
from db import goods_get_nickname, goods_get_avatar, goods_get_intcoins, goods_get_last_trades, goods_new_user_first_time, goods_set_avatar

logging.basicConfig(level=logging.INFO)
bot = Bot(token=goods_bot_token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

#PHOTO_SERVER_PATH = "/home/aboba/intcoin/web/IntCoin/static/uploads/"
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
    user_id = message.from_user.id
    user_nickname = goods_get_nickname(user_id)
    user_avatar = goods_get_avatar(user_id)
    user_avatar_file = InputFile(user_avatar)
    user_intcoins = goods_get_intcoins(user_id)
    user_last_trades = goods_get_last_trades(user_id)

    caption = f"{user_nickname}\n\nБаланс Инткоинов: {user_intcoins}\n\n{user_last_trades}"
    await message.answer_photo(photo=user_avatar_file, caption=caption)


@dp.message_handler(commands=["setavatar"])
async def cmd_setavatar(message: types.Message):
    is_setting = True
    await message.answer(text="Для смены аватарки, отправьте новое фото прямо сюда")

@dp.message_handler(content_types=[types.ContentType.PHOTO])
async def gen_avatar(message: types.Message):
    user_id = message.from_user.id
    user_avatar_filename = f"{user_id}.jpg"
    file_id = message.photo[-1].file_id
    file = await bot.download_file_by_id(file_id=file_id)
    with open(PHOTO_SERVER_PATH + user_avatar_filename, 'wb') as temp_file:
        temp_file.write(file.getvalue())

    # обработка фото (ВСТАВКА В РАМКУ)
    goods_set_avatar(user_avatar_filename, user_id)
    await message.answer(text="Фото успешно обновлено!")


@dp.message_handler(commands=["help"])
async def cmd_help(message: types.Message):
    await message.answer("/status - Получить краткую информацию об аккаунте\n/setavatar - Установить аватарку\n/setnickname - Установить никнейм\n/web - Открыть Магазин Ништяков, если кнопка меню недоступна\n")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    executor.start_polling(dp, skip_updates=True)
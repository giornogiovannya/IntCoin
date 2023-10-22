import asyncio
import json
import logging
import sys
from aiohttp import web
from aiogram import Bot, Dispatcher, types

import config
from config import goods_bot_token
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputFile
from db import goods_get_nickname, goods_get_avatar, goods_get_intcoins, goods_get_last_trades, goods_new_user_first_time, goods_set_avatar, goods_set_nickname, admin_get_orders, goods_transfer_coins
from aiogram.dispatcher.filters.state import StatesGroup, State
from PIL import Image, ImageDraw


logging.basicConfig(level=logging.INFO)
bot = Bot(token=goods_bot_token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

PHOTO_SERVER_PATH = "/home/aboba/intcoin/web/IntCoin/static/uploads/"


class SettersStates(StatesGroup):
    NICKNAME = State()
    AVATAR = State()
    TRANSFER = State()


@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
    goods_new_user_first_time(message.from_user.id, message.from_user.first_name)
    await message.answer("Привет! Для просмотра доступных комманд нажми /help")
    await cmd_help(message)


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
    user_avatar_file = InputFile(PHOTO_SERVER_PATH + user_avatar)
    user_intcoins = goods_get_intcoins(user_id)
    user_last_trades = goods_get_last_trades(user_id)

    caption = f"{user_nickname}\n\nБаланс Инткоинов: {user_intcoins}\n\n{user_last_trades}"
    await message.answer_photo(photo=user_avatar_file, caption=caption)
    await cmd_help(message)



@dp.message_handler(commands=['sendallready'])
async def cmd_send_all(message: types.Message):
    admin_id = config.admin_user_id
    if message.chat.id == admin_id:
        users = []
        for i in users:
            await bot.send_message(chat_id=i, text="Текст рассылки")
        orders = admin_get_orders()
        for order in orders:
            if 'Статус: Готово' in order:
                goods = order.split(',')[3].split(':')[1].strip()
                user_id = order.split(',')[1].split(':')[1].strip()
                order_id = order.split(',')[0].split(':')[1].strip()
                text = f"Ваш заказ {order_id}: {goods} готов к выдаче, пожалуйста, поднимитесь в кабинет."
                await bot.send_message(chat_id=user_id, text=text)

        await message.answer('Рассылка окончена')



@dp.message_handler(commands=["setavatar"])
async def cmd_setavatar(message: types.Message):
    await message.answer(text="Для смены аватарки, отправьте новое фото прямо сюда")
    await SettersStates.AVATAR.set()


@dp.message_handler(commands=["transfer"])
async def cmd_transfer(message: types.Message):
    await message.answer(text="Для отправки своих инткоинов, укажите их количество и никнейм получателя через пробел (Пример: 50 aboba)")
    await SettersStates.TRANSFER.set()


@dp.message_handler(state=SettersStates.TRANSFER)
async def tranfer(message: types.Message):
    to_id, coins_count = message.split(' ')
    from_id = message.from_user.id
    goods_transfer_coins(from_id, to_id, coins_count)
    await message.answer("Коины успешно отправлены!")
    await cmd_help(message)


@dp.message_handler(state=SettersStates.AVATAR, content_types=[types.ContentType.PHOTO])
async def gen_avatar(message: types.Message):
    user_id = message.from_user.id
    user_avatar_filename = f"{user_id}.jpg"
    file_id = message.photo[-1].file_id
    file = await bot.download_file_by_id(file_id=file_id)
    with open(PHOTO_SERVER_PATH + user_avatar_filename, 'wb') as temp_file:
        temp_file.write(file.getvalue())

    background = Image.new('RGB', (1000, 1000), 'black')
    image = Image.open(PHOTO_SERVER_PATH + user_avatar_filename)
    mask = Image.new('L', (600, 600), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, 600, 600), fill=255)
    image = image.resize((600, 600))
    image.putalpha(mask)
    offset = (200, 200)
    background.paste(image, offset, image)
    background.save(f'{user_id}_temp.jpg')
    background = Image.open(f'{user_id}_temp.jpg')
    frame = Image.open('intensa.png')
    background.paste(frame, (0, 0), frame)
    background.save(PHOTO_SERVER_PATH + user_avatar_filename)

    goods_set_avatar(user_avatar_filename, user_id)
    await message.answer(text="Фото успешно обновлено!")
    await dp.current_state(user=message.from_user.id).finish()


@dp.message_handler(commands=["help"])
async def cmd_help(message: types.Message):
    await message.answer("/status - Получить краткую информацию об аккаунте\n/setavatar - Установить аватарку\n/setnickname - Установить никнейм\n/web - Открыть Магазин Ништяков, если кнопка меню недоступна\n")


@dp.message_handler(commands=['setnickname'])
async def cmd_set_nickname(message: types.Message):
    await message.reply("Введите новый никнейм:")
    await SettersStates.NICKNAME.set()


@dp.message_handler(state=SettersStates.NICKNAME)
async def save_nickname(message: types.Message):
    user_id = message.from_user.id
    updated_nickname = message.text
    goods_set_nickname(updated_nickname, user_id)
    await message.reply(f"Ваш новый никнейм: {updated_nickname}")
    await dp.current_state(user=message.from_user.id).finish()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    executor.start_polling(dp, skip_updates=True)
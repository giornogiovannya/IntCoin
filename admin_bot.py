import secrets
import sqlite3
import hashlib
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher.filters import Text
from aiogram.types import CallbackQuery, ContentType, InputMediaPhoto
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import config
from config import admin_bot_token
from aiogram.types import InputFile
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram_dialog.widgets.kbd import Button, Cancel, SwitchTo, Row
from aiogram_dialog.widgets.text import Const
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog import Window, Dialog, DialogRegistry, DialogManager, StartMode, ShowMode
from db import admin_addnew_goods, admin_addnew_unique_goods, admin_get_orders, admin_get_users_count, \
    admin_get_user_info
from PIL import Image, ImageDraw

bot = Bot(token=admin_bot_token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(LoggingMiddleware())
sizes_dict = {"S": 0, "M": 0, "L": 0, "XL": 0, "XXL": 0}
current_size = ""
is_sizable_merch = False
registry = DialogRegistry(dp)

PHOTO_SERVER_PATH = "/home/aboba/intcoin/web/IntCoin/static/uploads/"


class AddGoodsDialog(StatesGroup):
    goods_category = State()
    goods_merch_size = State()
    goods_title = State()
    goods_description = State()
    goods_count = State()
    goods_photo = State()
    goods_cost = State()
    goods_approve = State()
    goods_generate_preview = State()
    merch_set_size = State()


async def push_goods_to_db(goods_info):
    global sizes_dict
    global is_sizable_merch
    is_sizable_merch = False
    total_count = sum(sizes_dict.values())
    sizes_dict = {"S": 0, "M": 0, "L": 0, "XL": 0, "XXL": 0}
    try:
        admin_addnew_goods(goods_info)
        admin_addnew_unique_goods(goods_info, total_count)
    except sqlite3.Error as e:
        print(e)


async def on_goods_title(message: types.Message, dialog: Dialog, manager: DialogManager):
    user_data = manager.current_context().dialog_data
    user_data["goods_title"] = message.text
    await dialog.next()


async def on_goods_description(message: types.Message, dialog: Dialog, manager: DialogManager):
    global is_sizable_merch
    user_data = manager.current_context().dialog_data
    user_data["goods_description"] = message.text
    if is_sizable_merch:
        await dialog.switch_to(AddGoodsDialog.goods_photo)
    else:
        await dialog.switch_to(AddGoodsDialog.goods_count)


async def on_goods_count(message: types.Message, dialog: Dialog, manager: DialogManager):
    user_data = manager.current_context().dialog_data
    user_data["goods_count"] = message.text
    await manager.dialog().switch_to(AddGoodsDialog.goods_photo)


async def get_goods_info_from_manager(manager: DialogManager):
    goods_info = [
        manager.current_context().dialog_data.get("goods_hash", ""),
        manager.current_context().dialog_data.get("goods_category", ""),
        manager.current_context().dialog_data.get("goods_title", ""),
        manager.current_context().dialog_data.get("goods_description", ""),
        manager.current_context().dialog_data.get("goods_merch_size", ""),
        manager.current_context().dialog_data.get("goods_count", ""),
        manager.current_context().dialog_data.get("goods_photo", ""),
        manager.current_context().dialog_data.get("goods_cost", ""),
    ]
    goods_keys = ["goods_hash", "goods_category", "goods_title", "goods_description", "goods_merch_size",
                  "goods_count", "goods_photo", "goods_cost"]
    goods_dict = dict(zip(goods_keys, goods_info))
    return goods_dict, goods_keys


async def on_goods_cost(message: types.Message, dialog: Dialog, manager: DialogManager):
    user_data = manager.current_context().dialog_data
    user_data["goods_cost"] = message.text

    goods_category = manager.current_context().dialog_data.get("goods_category", "")
    if goods_category == "merch":
        goods_dict, goods_keys = await get_goods_info_from_manager(manager)
        goods_list = []
        if any(count > 0 for size, count in sizes_dict.items()):
            for size, count in sizes_dict.items():
                if count > 0:
                    goods_info = [
                        manager.current_context().dialog_data.get("goods_hash", ""),
                        manager.current_context().dialog_data.get("goods_category", ""),
                        manager.current_context().dialog_data.get("goods_title", ""),
                        manager.current_context().dialog_data.get("goods_description", ""),
                        size,
                        count,
                        manager.current_context().dialog_data.get("goods_photo", ""),
                        manager.current_context().dialog_data.get("goods_cost", ""),
                    ]
                    goods_dict = dict(zip(goods_keys, goods_info))
                    goods_list.append(goods_dict)
                    goods = goods_list
        else:
            goods = goods_dict
    else:
        goods_dict, goods_keys = await get_goods_info_from_manager(manager)
        goods = goods_dict
    formatted_string = f"{goods_dict['goods_title']}\n{goods_dict['goods_description']}\n{goods_dict['goods_cost']}"
    user_data['goods_info'] = goods
    photo = InputFile(PHOTO_SERVER_PATH + goods_dict['goods_photo'])
    await message.answer_photo(photo=photo, caption=formatted_string)
    await dialog.next()


async def on_goods_photo(message: types.Message, dialog: Dialog, manager: DialogManager):
    user_data = manager.current_context().dialog_data
    goods_hash = user_data["goods_hash"]
    filename = f"{goods_hash}.jpg"
    file_id = message.photo[-1].file_id
    file = await bot.download_file_by_id(file_id=file_id)
    with open(PHOTO_SERVER_PATH + filename, 'wb') as temp_file:
        temp_file.write(file.getvalue())
    user_data['goods_photo'] = filename
    await dialog.switch_to(AddGoodsDialog.goods_cost)


async def success(callback: CallbackQuery, button: Button, manager: DialogManager):
    manager.show_mode = ShowMode.EDIT
    goods_info = manager.current_context().dialog_data.get("goods_info")
    await callback.message.answer(text="Ништяк успешно добавлен!")
    await push_goods_to_db(goods_info)
    await manager.done()
    await cmd_help(callback.message)


async def set_placeholder(callback: CallbackQuery, button: Button, manager: DialogManager):
    user_data = manager.current_context().dialog_data
    user_data["goods_photo"] = "placeholder.jpg"
    await manager.dialog().switch_to(AddGoodsDialog.goods_cost)


async def choose_category(callback: CallbackQuery, button: Button, manager: DialogManager):
    user_data = manager.current_context().dialog_data
    goods_category = button.widget_id
    random_bytes = secrets.token_bytes(16)
    hash_sha256 = hashlib.sha256(random_bytes).hexdigest()
    user_data["goods_hash"] = hash_sha256[:16]
    user_data["goods_category"] = button.widget_id
    print(user_data['goods_category'])
    if goods_category == "merch":
        await manager.dialog().switch_to(AddGoodsDialog.goods_merch_size)
    else:
        await manager.dialog().switch_to(AddGoodsDialog.goods_title)


async def choose_size(callback: CallbackQuery, button: Button, manager: DialogManager):
    global is_sizable_merch
    merch_size_status = button.widget_id
    if merch_size_status == "with_size":
        is_sizable_merch = True
        keyboard = await update_keyboard()
        await callback.message.answer(text="Выберите размер, после чего измените наличие товара:", reply_markup=keyboard)
        await manager.dialog().switch_to(AddGoodsDialog.goods_title)
    if merch_size_status == "without_size":
        await manager.dialog().switch_to(AddGoodsDialog.goods_title)


async def update_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=3)
    for size, quantity in sizes_dict.items():
        text = f"{size}: {quantity}"
        if size == current_size:
            text += " (Текущий)"
        button = types.InlineKeyboardButton(text, callback_data=f"select_size_{size}")
        keyboard.insert(button)
    keyboard.row(
        types.InlineKeyboardButton("+", callback_data="increase_quantity"),
        types.InlineKeyboardButton("-", callback_data="decrease_quantity")
    )
    keyboard.row(types.InlineKeyboardButton("Подтвердить", callback_data="confirm"))
    return keyboard


@dp.callback_query_handler(lambda callback: callback.data.startswith('select_size_'))
async def select_size(callback: types.CallbackQuery):
    global current_size
    current_size = callback.data.split('_')[-1]
    await bot.answer_callback_query(callback.id, f"Выбран размер: {current_size}")
    await callback.message.edit_reply_markup(await update_keyboard())


@dp.callback_query_handler(lambda callback: callback.data in ['increase_quantity', 'decrease_quantity'])
async def change_quantity(callback: types.CallbackQuery):
    action = callback.data
    if current_size:
        if action == 'increase_quantity':
            sizes_dict[current_size] += 1
        elif action == 'decrease_quantity':
            if sizes_dict[current_size] > 0:
                sizes_dict[current_size] -= 1
        await callback.message.edit_reply_markup(await update_keyboard())


@dp.callback_query_handler(lambda callback: callback.data == 'confirm')
async def confirm(callback: CallbackQuery):
    await bot.answer_callback_query(callback.id, "Информация сохранена")
    await callback.message.delete()

dialog = Dialog(
    Window(
        Const("Выберите категорию"),
        Row(
            Button(Const("Мерч"), id="merch", on_click=choose_category),
            Button(Const("Персональный бонус"), id="personal_bonus", on_click=choose_category),
            Button(Const("Путёвка"), id="travel", on_click=choose_category),
        ),
        state=AddGoodsDialog.goods_category,
    ),
    Window(
        Const("Название товара"),
        MessageInput(on_goods_title),
        state=AddGoodsDialog.goods_title,
    ),
    Window(
        Const("Описание товара"),
        MessageInput(on_goods_description),
        state=AddGoodsDialog.goods_description,
    ),
    Window(
        Const("Количество товара в наличии (числом)"),
        MessageInput(on_goods_count),
        state=AddGoodsDialog.goods_count,
    ),
    Window(
        Const("Ништяк имеет размерную сетку ?"),
        Button(Const("Размерный"), id="with_size", on_click=choose_size),
        Button(Const("Безразмерный"), id="without_size", on_click=choose_size),
        state=AddGoodsDialog.goods_merch_size,
    ),
    Window(
        Const("Пришлите фото ништяка, либо выберите готовое"),
        Button(Const("Хватит и плейсхолдера"), id="without_photo", on_click=set_placeholder),
        MessageInput(on_goods_photo, content_types=[ContentType.PHOTO]),
        state=AddGoodsDialog.goods_photo,
    ),
    Window(
        Const("Количество инткоинов, необходимых для покупки ништяка"),
        MessageInput(on_goods_cost),
        state=AddGoodsDialog.goods_cost,
    ),
    Window(
        Const("Карточка будем иметь следующий вид"),
        Button(Const("Сохранить"), id="saveCard", on_click=success),
        SwitchTo(Const("Начать заново"), id="restartCard", state=AddGoodsDialog.goods_title),
        state=AddGoodsDialog.goods_approve,
        preview_add_transitions=[Cancel()],
    ),
)

registry.register(dialog)


@dp.message_handler(Text(equals="Добавить награду"))
async def handler_addnewreward(message: types.Message, dialog_manager: DialogManager):
    await dialog_manager.start(AddGoodsDialog.goods_category, mode=StartMode.RESET_STACK)


@dp.message_handler(commands=["addnewreward"])
async def cmd_addnewreward(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[[
        types.KeyboardButton(text="Добавить награду"), ], ],
                                         one_time_keyboard=True)
    await message.answer("Текст",
                         reply_markup=keyboard)


@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
    await message.answer("hello")


@dp.message_handler(commands=["help"])
async def cmd_help(message: types.Message):
    await message.answer("/getrewards - Получить список наград\n/addnewreward - Добавить новую награду\n/gettasks - Получить список заданий\n/addnewtask - Добавить новое задание\n/watchuserslist - Получить список сотрудников и выдать баллы\n/getorders - Получить список заказов сотрудников\n/sendallready - Разослать оповещение всем сотрудникам, чей статус заказа: \"Готово к выдаче\"")


@dp.message_handler(commands=['getorders'])
async def cmd_get_orders(message: types.Message):
    orders_arr = admin_get_orders()
    orders_list_str = "\n\n".join(orders_arr)
    await message.answer(orders_list_str)


@dp.message_handler(commands=['watchuserslist'])
async def cmd_watch_users_list(message: types.Message):
    user_number = 1
    markup = types.InlineKeyboardMarkup().add(
        types.InlineKeyboardButton("Назад", callback_data=f"previous_user:0"),
        types.InlineKeyboardButton("Вперёд", callback_data=f"next_user:1")
    )
    markup.row(types.InlineKeyboardButton("Начислить", callback_data=f"add"))
    markup.row(types.InlineKeyboardButton("Убавить", callback_data=f"remove"))
    inff = admin_get_user_info(user_number)
    user_nickname, user_avatar, user_intcoins = inff[2], inff[3], inff[4]
    user_caption = f"Ник: {user_nickname}\nБаланс: {user_intcoins}"
    user_avatar_filesystem_path = PHOTO_SERVER_PATH + user_avatar
    await message.answer_photo(photo=InputFile(user_avatar_filesystem_path), caption=user_caption, reply_markup=markup, parse_mode="Markdown")


@dp.message_handler(commands=['sendallready'])
async def cmd_send_all(message: types.Message):
    admin_id = config.admin_user_id
    if message.chat.id == admin_id:
        await message.answer("Рассылка запущена")
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
    else:
        await message.answer('Ошибка авторизации')


@dp.callback_query_handler(text_startswith="add")
async def hdr_add_intcoins(call: types.CallbackQuery):
    print(call)
    print(call)


@dp.callback_query_handler(text_startswith="previous_user")
async def hdr_previous_user(call: types.CallbackQuery):
    user_number = int(call.data.split(":")[1]) - 1
    if user_number < 1:
        last_user_number = admin_get_users_count()
        await show_current_user(call.message, call.from_user['id'], call.id, last_user_number)
    else:
        await show_current_user(call.message, call.from_user['id'], call.id, user_number)


@dp.callback_query_handler(text_startswith="next_user")
async def hdr_next_user(call: types.CallbackQuery):
    user_number = int(call.data.split(":")[1]) + 1
    await show_current_user(call.message, call.from_user['id'], call.id, user_number)


async def show_current_user(message, user_id, call_id, user_number):
    users_count = admin_get_users_count()
    markup = types.InlineKeyboardMarkup().add(
        types.InlineKeyboardButton("Назад", callback_data=f"previous_user:{user_number}"),
        types.InlineKeyboardButton("Вперёд", callback_data=f"next_user:{user_number}")
    )
    markup.row(types.InlineKeyboardButton("Начислить", callback_data=f"add"))
    markup.row(types.InlineKeyboardButton("Убавить", callback_data=f"remove"))
    if not user_number > users_count:
        inff = admin_get_user_info(user_number)
        user_nickname, user_avatar, user_intcoins = inff[2], inff[3], inff[4]
        user_avatar_filesystem_path = PHOTO_SERVER_PATH + user_avatar
        user_caption = f"Ник: {user_nickname}\nБаланс: {user_intcoins}"
        user_avatar_file_input_media = InputMediaPhoto(media=InputFile(user_avatar_filesystem_path), caption=user_caption, parse_mode="Markdown")
        await message.edit_media(user_avatar_file_input_media, reply_markup=markup)
    else:
        await show_current_user(message, user_id, call_id, user_number=1)


if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)

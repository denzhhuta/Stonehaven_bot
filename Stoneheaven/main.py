import aiogram
import time
import os
from aiogram import types, Bot, Dispatcher, executor
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types import CallbackQuery
from conf import TOKEN_API
from conf import CONTACTS_COMMAND
from keyboard import kb
from keyboard import get_inline_keyboard
from conf import MEDIA_COMMAND
import aiomysql
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from datetime import datetime
from database import connect_to_db

storage = MemoryStorage()
bot = aiogram.Bot(TOKEN_API)
dp = aiogram.Dispatcher(bot, storage=storage)

# Initialize the bot


async def on_startup(_):
    print("Bot was succesfully lauched!")

@dp.message_handler(commands=['start']) 
async def start_command(message: types.Message):
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    
    if last_name is None:
        await bot.send_message(chat_id=message.from_user.id,
                           text=f"<b>Добро пожаловать, {message.from_user.first_name}!</b>",
                           parse_mode="HTML",
                           reply_markup=kb)
    else:
        await bot.send_message(chat_id=message.from_user.id,
                           text=f"<b>Добро пожаловать, {message.from_user.first_name} {message.from_user.last_name}!</b>",
                           parse_mode="HTML",
                           reply_markup=kb)

@dp.message_handler(text='Информация сервера 📱')
async def server_info(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text='<b>Меню информации по серверу</b>',
                           parse_mode="HTML",
                           reply_markup=get_inline_keyboard())
    await message.delete()

#Функция и
@dp.message_handler(text='Информация об игроках 👀')
async def player_info(message: types.Message, state: FSMContext):
    msg = await bot.send_message(chat_id=message.from_user.id,
                           text="Пожалуйста, введите имя игрока")
    await message.delete()
    await state.set_state('await_input_nickname')
    
@dp.message_handler(state="await_input_nickname")
async def input_name(message: types.Message, state: FSMContext):
    nickname = message.text
    await state.update_data(nickname=nickname)
    await state.reset_state()
    
    conn = await connect_to_db()
    
    async with conn.cursor() as cursor:
        #Якщо бещ COLLATE, то помилка
        #pymysql.err.OperationalError: (1267, "Illegal mix of collations 
        #(utf8mb3_general_ci,IMPLICIT) and (utf8mb4_general_ci,COERCIBLE) for operation '='")
        sql = "SELECT * FROM authme WHERE username=%s COLLATE utf8mb4_general_ci"
        #sql = "SELECT * FROM authme WHERE username=%s"
        await cursor.execute(sql, (nickname,))
        result = await cursor.fetchone()
        
    conn.close()
    
    STUCTURED_MESSAGE = """
    <b>Информация о пользователе:</b>
    <b>Ник: {username}</b>
    <b>IP адрес: {ip}</b>
    <b>Последний вход: {lastlogin}</b>
    <b>Дата регистрации: {regdate}</b>
    <b>Статус: {isLogged}</b>
    """

    if result:
        logged_dict = {'0':'Оффлайн ❌', '1':'Онлайн ✅'}
        timestamp_regdate = result['regdate'] / 1000
        regdate = datetime.fromtimestamp(timestamp_regdate)
        formatted_date_regdate = regdate.strftime("%Y-%m-%d %H:%M:%S")
    
        timestamp_lastlogin = result['lastlogin'] / 1000
        regdate_lastlogin = datetime.fromtimestamp(timestamp_lastlogin)
        formatted_date_lastlogin = regdate_lastlogin.strftime("%Y-%m-%d %H:%M:%S")
        #Dictionary, якщо 1 - Онлайн, 0 - Оффлайн, якщо немає співпадінь, то повертає пусту лінійку
        #тому пишемо ''
        is_logged_text = logged_dict.get(str(result['isLogged']), '')
        message_text = STUCTURED_MESSAGE.format(
            username=result['username'],
            realname=result['realname'],
            ip=result['ip'],
            lastlogin=formatted_date_lastlogin,
            regdate=formatted_date_regdate,
            isLogged=is_logged_text
            )
        await bot.send_message(chat_id=message.chat.id, 
                               text=message_text, 
                               parse_mode='HTML')
    else:
        await bot.send_message(chat_id=message.chat.id, 
                               text='<b>Пользователь не найден. Пожалуйста, проверьте учетные данные!</b>',
                               parse_mode='HTML')
        



@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('info'))
async def ikb_cb_handler(callback: types.CallbackQuery):
 try:
    if callback.data == "info_contacts":
        await callback.message.edit_text(CONTACTS_COMMAND,
                                         parse_mode="HTML",
                                         disable_web_page_preview=True,
                                         reply_markup=get_inline_keyboard())
    elif callback.data == "info_media":
        await callback.message.edit_text(MEDIA_COMMAND,
                                         parse_mode="HTML",
                                         disable_web_page_preview=True,
                                         reply_markup=get_inline_keyboard())
    else:
        raise ValueError("Invalid button pressed")
    
 except Exception as e:
    pass    


if __name__ == '__main__':
    executor.start_polling(dp, 
                           on_startup=on_startup, 
                           skip_updates=True)    

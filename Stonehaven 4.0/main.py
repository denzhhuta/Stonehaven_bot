import aiogram
import aiomysql
import hashlib
from hashlib import sha256
import secrets
from email.message import EmailMessage
from aiosmtplib import SMTP
import time
import os
from aiogram import types, Bot, Dispatcher, executor
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types import CallbackQuery
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from conf import MEDIA_COMMAND
from conf import TOKEN_API
from conf import CONTACTS_COMMAND
from conf import EMAIL_NOTIFY
from keyboard import kb
from keyboard import get_inline_keyboard
from datetime import datetime
from database import connect_to_db
from database import get_user_info
from database import is_valid_email
from database import new_password_db
from emails import generate_confirmation_code
from emails import send_email

storage = MemoryStorage()
bot = aiogram.Bot(TOKEN_API)
dp = aiogram.Dispatcher(bot, storage=storage)

# class ProfileStatesGroup(StatesGroup):
#     input_email = State()
#     confirmation_code = State()

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
    
    message_text = await get_user_info(nickname)
    await bot.send_message(chat_id=message.from_user.id,
                           text=message_text,
                           parse_mode="HTML")
    
@dp.message_handler(text='Восстановление пароля 🔧')
async def forgot_password_handle(message: types.Message, state:FSMContext):
    await message.reply("<b>Пожалуйста, введите email-адресс вашего аккаунта</b>",
                        parse_mode="HTML")
    await message.delete()
    await state.set_state('input_email')

@dp.message_handler(state="input_email")
async def input_name(message: types.Message, state: FSMContext):
    email = message.text
    await state.update_data(email=email)
    #print("CHINAAA " + email)    
    #await state.reset_state()
    if not await is_valid_email(email):
          await bot.send_message(chat_id=message.from_user.id,
                                text="<b>🙁 Извините, <em>электронная почта</em> недействительна!</b>\n\n<b>🔍 Перепроверьте правильность ввода!</b>",
                                parse_mode="HTML")
          await state.reset_state()
          return
    
    confirmation_code = await generate_confirmation_code()
    print("CHINAAA " + confirmation_code)
    await send_email(email, confirmation_code)
    await state.update_data(confirmation_code=confirmation_code)
    await state.set_state('confirmation_code_proof')

    await bot.send_message(chat_id=message.from_user.id,                  
                           text=EMAIL_NOTIFY,
                           parse_mode="HTML")
    
@dp.message_handler(state="confirmation_code_proof")
async def confirm_code(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        email = data.get('email')
        confirmation_code = data.get('confirmation_code')
    
    #print("China " + email) 
    #print("China " + confirmation_code) 
    
    if message.text != confirmation_code:
        await bot.send_message(chat_id=message.from_user.id,
                               text="<b>🙁Извините, <em>код подтверждения</em> недействительный!</b>\n\n<b>🔍Перепроверьте правильность ввода!</b>",
                               parse_mode="HTML")
        await state.reset_state()
    else:
        await bot.send_message(chat_id=message.from_user.id,
                               text="<b>Код подтверждения действителен. Введите новый пароль!\nЕсли вы передумали менять пароль, напишите /cancel.</b>",
                               parse_mode="HTML")
        await state.set_state('password_update_new')

@dp.message_handler(state='password_update_new')
async def password_update(message: types.Message, state: FSMContext):
    password = message.text
    
    if str(password) == '/cancel':
        await bot.send_message(chat_id=message.from_user.id,
                               text="<b>Операция отменена!</b>",
                               parse_mode="HTML")
        await state.reset_state()
        return
            
    if len(password) < 8:
        await bot.send_message(chat_id=message.from_user.id,
                                text="<b>Пароль слишком короткий!</b>",
                                parse_mode="HTML")
        #await state.update_data(salt=salt)
        await bot.send_message(chat_id=message.from_user.id,
                                text="<b>Пожалуйста, введите новый пароль (минимум 8 символов).</b>",
                                parse_mode="HTML")
        await state.set_state('password_update_new')
        return
    
    await state.update_data(password=password)
    
    await bot.send_message(chat_id=message.from_user.id,
                            text="<b>Пожалуйста, повторите новый пароль!</b>",
                            parse_mode="HTML")
    await state.set_state('password_update_confirm')
    
@dp.message_handler(state='password_update_confirm')
async def password_update(message: types.Message, state: FSMContext):   
    confirm_password = message.text
    #data = await state.get_data()
    async with state.proxy() as data:
        password = data.get('password')
        email = data.get('email')
    
    if str(confirm_password) == '/cancel':
        await bot.send_message(chat_id=message.from_user.id,
                               text="<b>Операция отменена!</b>",
                               parse_mode="HTML")
        await state.reset_state()
        return
            
    if confirm_password == password:
        salt = secrets.token_hex(8)
        hex_dig = hashlib.sha256((hashlib.sha256(password.encode('utf-8')).hexdigest() + salt).encode('utf-8')).hexdigest()
        hashed_password = f"$SHA${salt}${hex_dig}"
        #print(hashed_password)
        #print(email)
        #print(password)
        await new_password_db(hashed_password, email)
        await bot.send_message(chat_id=message.from_user.id,
                                text="<b>Пароль успешно обновлен</b>",
                                parse_mode="HTML")
        await state.reset_state()

    else:
        await bot.send_message(chat_id=message.from_user.id,
                                text="<b>Пароли не совпадают, повторите попытку</b>",
                                parse_mode="HTML")
        await state.set_state('password_update_confirm')
    
    # print(salt)
    # hash_object = hashlib.sha256((salt + password).encode('utf-8'))
    # hexdig = hash_object.hexdigest()
    # new_password = f"$SHA${salt}${hex_dig}"
    # print(new_password)
    # await state.reset_state()
    
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
    executor.start_polling(dp, skip_updates=True)    

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
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.dispatcher.handler import CancelHandler
from aiogram.types import Update
from aiogram.types.chat_member import ChatMemberMember, ChatMemberOwner, ChatMemberAdministrator
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types import CallbackQuery
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from conf import MEDIA_COMMAND
from conf import TOKEN_API
from conf import CONTACTS_COMMAND
from conf import EMAIL_NOTIFY
from conf import CHANNEL_ID
from keyboard import kb
from keyboard import get_inline_keyboard_1
from keyboard import get_inline_keyboard_2
from datetime import datetime
from database import connect_to_db
from database import get_user_info
from database import is_valid_email
from database import new_password_db
from email_function import generate_confirmation_code
from email_function import send_email
from email_function import check_server

#update_message_text - просто текст шо пише юзер
#update.message.from_user - dict з username, last_name, is_bot and so on
#{"id": 1013673667, "is_bot": false, "first_name": "Denis", "last_name": "Zhhuta", "username": "morkovka2005", "language_code": "uk"}
#{"update_id": 744326143, "message": {"message_id": 1261, "from": {"id": 1013673667, "is_bot": false, "first_name": "Denis", "last_name": "Zhhuta", "username": "morkovka2005", "language_code": "uk"}, "chat": {"id": 1013673667, "first_name": "Denis", "last_name": "Zhhuta", "username": "morkovka2005", "type": "private"}, "date": 1680552731, "text": "а"}}
class CheckSubscriptionUserMiddleware(BaseMiddleware):
    def __init__(self):
         self.prefix = 'key_prefix'
         super(CheckSubscriptionUserMiddleware, self).__init__()
        
    async def on_process_update(self, update: types.Update, data: dict):
        if "message" in update:
            this_user = update.message.from_user
            if update.message.text:
                if "start" in update.message.text:
                    return
                
        elif "callback_query" in update:
            this_user = update.callback_query.from_user
        
        else:
            this_user = None
            
        if this_user is not None:
            get_prefix = self.prefix
            
            if not this_user.is_bot:
                user_id = this_user.id
                #print(user_id)
                check_user_in_channel = await bot.get_chat_member(CHANNEL_ID, user_id)
                #print(check_user_in_channel)
                #isinstance юзається щоб перевірити одне від іншого, в нашому випадку чи чек юзер іт ін ченел є мембер
                #{"user": {"id": 6119267627, "is_bot": false, "first_name": "Maks", "username": "maksik42413", "language_code": "uk"}, "status": "member"}
                if not isinstance(check_user_in_channel, ChatMemberMember) and not isinstance(check_user_in_channel, ChatMemberOwner) and not isinstance(check_user_in_channel, ChatMemberAdministrator):
                    await bot.send_message(user_id, 
                                           "<b>😔 Для использования нашего бота вам необходимо быть подписанным на нашу группу в Telegram!</b>", 
                                           parse_mode="HTML",
                                           reply_markup=get_inline_keyboard_2())
                    raise CancelHandler()
                
                   
storage = MemoryStorage()
bot = aiogram.Bot(TOKEN_API)
dp = aiogram.Dispatcher(bot, storage=storage)
    
@dp.message_handler(commands=['start'])
async def start_command(message: types.Message) -> None:
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
async def server_info(message: types.Message) -> None:
    await bot.send_message(chat_id=message.from_user.id,
                           text='<b>Меню информации по серверу</b>',
                           parse_mode="HTML",
                           reply_markup=get_inline_keyboard_1())
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
      
@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('info'))
async def ikb_cb_handler(callback: types.CallbackQuery):
 try:
    if callback.data == "info_contacts":
        await callback.message.edit_text(CONTACTS_COMMAND,
                                         parse_mode="HTML",
                                         disable_web_page_preview=True,
                                         reply_markup=get_inline_keyboard_1())
    elif callback.data == "info_media":
        await callback.message.edit_text(MEDIA_COMMAND,
                                         parse_mode="HTML",
                                         disable_web_page_preview=True,
                                         reply_markup=get_inline_keyboard_1())
    elif callback.data == "info_online":
        ip_address = "193.169.195.76"
        port = 25565
        message_text = await check_server(ip_address, port)
        await callback.message.edit_text(message_text,
                                         parse_mode="HTML",
                                         disable_web_page_preview=True,
                                         reply_markup=get_inline_keyboard_1())
    else:
        raise ValueError("Invalid button pressed")
    
 except Exception as e:
    pass    

if __name__ == '__main__':
    dp.middleware.setup(CheckSubscriptionUserMiddleware())
    executor.start_polling(dp, 
                           skip_updates=True)    

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

bot = aiogram.Bot(TOKEN_API)
dp = aiogram.Dispatcher(bot)

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

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup

def get_inline_keyboard() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton('Наши сойцсети 📱', callback_data='info_media'),
         InlineKeyboardButton('Контакты 🤖', callback_data='info_contacts')]
        ])
    return ikb


kb = ReplyKeyboardMarkup(resize_keyboard=True)
b1 = KeyboardButton(text="Информация сервера 📱")
b2 = KeyboardButton(text="Информация об игроках 👀")
b3 = KeyboardButton(text="Восстановление пароля 🔧")
kb.add(b1).add(b2).insert(b3)
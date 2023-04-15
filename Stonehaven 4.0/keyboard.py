from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup

def get_inline_keyboard_1() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton('Наши соцсети 📱', callback_data='info_media'),
         InlineKeyboardButton('Контакты 🤖', callback_data='info_contacts')],
        [InlineKeyboardButton('Онлайн сервера 📈', callback_data='info_online')]
    ])
    return ikb

def get_inline_keyboard_2() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton('👉 Подписаться', url='https://t.me/+qJA3_fKo1pJmM2Ey')]
    ])
    return ikb

kb = ReplyKeyboardMarkup(resize_keyboard=True)
b1 = KeyboardButton(text="Информация сервера 📱")
b2 = KeyboardButton(text="Информация об игроках 👀")
b3 = KeyboardButton(text="Восстановление пароля 🔧")
kb.add(b1).add(b2).insert(b3)
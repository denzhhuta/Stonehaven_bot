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
b4 = KeyboardButton(text="Игроки онлайн 🌟")
b5 = KeyboardButton(text="Управление сервером")
kb.add(b1).add(b2).insert(b3).add(b4).insert(b5)


def on_players_online_press() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    b1 = KeyboardButton(text="Посмотреть полный лист игроков 📃")
    b2 = KeyboardButton(text="Найти игрока по никнейму 🔍")
    back_button = KeyboardButton(text="Назад 🔙")
    kb.add(b1).add(b2).insert(back_button)
    return kb

def server_rcon() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    b1 = KeyboardButton(text="Забанить игрока")
    b2 = KeyboardButton(text="Кикнуть игрока")
    b3 = KeyboardButton(text="Уведомить игроков")
    back_button = KeyboardButton(text="Назад 🔙")
    kb.add(b1).add(b2).insert(back_button).insert(b3)
    return kb
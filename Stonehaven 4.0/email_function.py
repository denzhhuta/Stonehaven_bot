from email.message import EmailMessage
from aiosmtplib import SMTP
import aiomysql
import random
import string
import asyncio
import aiohttp
import aiogram
from conf import sender_email
from conf import app_password
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from mcstatus import JavaServer

#функція надсилання повідомлення на пошту гравця
async def send_email(email: str, confirmation_code: str):
    html = f'''
        <html>
        <head>
        <style>
            .container {{
            max-width: 500px;
            margin: 0 auto;
            background-color: #f1f1f1;
            border-radius: 10px;
            padding: 20px;
            }}

            .confirmation-code {{
            background-color: #4CAF50;
            color: #ffffff;
            font-weight: bold;
            font-size: 30px;
            text-align: center;
            padding: 20px;
            border-radius: 10px;
            }}

            @media only screen and (max-width: 600px) {{
            .container {{
                max-width: 100%;
            }}
            }}
        </style>
        </head>
        <body>
        <div class="container">
            <div class="confirmation-code">{confirmation_code}</div>
            <p>Ваш код подтверждения</p>
            <p>С уважением, команда проекта Stonehaven.</p>
        </div>
        </body>
        </html>
        '''
    msg = EmailMessage()
    msg['Subject'] = 'Stonehaven | Password Recovery'
    msg['From'] = sender_email
    msg['To'] = email
    msg.set_content(html, subtype='html')
    
    async with SMTP(hostname='smtp.gmail.com', port=587, start_tls=True,
                    username=sender_email, password=app_password) as smtp:
        await smtp.send_message(msg)
        
#Генерація рандомного коду
async def generate_confirmation_code() -> str:
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))

# #перевірка онлайна сервера
# async def check_server(ip_address, port):
#     url = f"https://api.mcsrvstat.us/2/{ip_address}:{port}"
#     async with aiohttp.ClientSession() as session:
#         async with session.get(url) as response:
#             if response.status == 200:
#                 data = await response.json()
#                 if data["online"]:
#                     status = "Online"
#                     players_online = data['players']['online']
#                     max_players = data['players']['max']
#                     message_text = (f"<b>Статус сервера:</b>\n"
#                                     f"<b>IP-адрес:</b> {ip_address}\n"
#                                     f"<b>Статус:</b> {status}  ✅\n"
#                                     f"<b>Игроков онлайн:</b> {players_online}/{max_players}")
#                 else:
#                     message_text = "<b>😔 Сервер временно недоступен!\nВедуться работы по оптимизации.\nПриносим свои извинения.</b>"
#             else:
#                 message_text = f"Error: {response.status}"
    
#     # Create a message object
#     #message = await bot.send_message(chat_id=message.from_user.id,
#                                      #text=message_text)
#     return message_text

async def check_server(ip_address, port):
    try:
        server = JavaServer.lookup(f"{ip_address}:{port}")
        status_servera = server.status()

        if status_servera:            
            status = "Online"
            players_online = status_servera.players.online
            max_players = status_servera.players.max
            message_text = (f"<b>Статус сервера:</b>\n"
                            f"<b>IP-адрес:</b> {ip_address}\n"
                            f"<b>Статус:</b> {status}  ✅\n"
                            f"<b>Игроков онлайн:</b> {players_online}/{max_players}")
        else:
            message_text = "<b>😔 Сервер временно недоступен!\nВедуться работы по оптимизации.\nПриносим свои извинения.</b>"
            
    except Exception as e:        
        message_text = f"<b>❌ Ошибка при проверке онлайна: {e}</b>"
    
    return message_text
            
        
        

async def check_online(ip_address, port, player_name):
    try:
        server = JavaServer.lookup(f"{ip_address}:{port}")
        query = server.query()

        if query.players:
            if player_name in query.players.names:
                message_text = f"<b>✅ {player_name} сейчас на сервере!</b>"
            else:
                message_text = f"<b>❌ {player_name} сейчас оффлайн!</b>"
        else:
            message_text = "<b>❌ Сервер сейчас оффлайн!</b>"
    except Exception as e:
        message_text = f"<b>❌ Ошибка при проверке онлайна: {e}</b>"

    return message_text


    
    
 
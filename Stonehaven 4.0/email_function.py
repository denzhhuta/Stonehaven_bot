from email.message import EmailMessage
from aiosmtplib import SMTP
import aiomysql
import random
import string
import asyncio
from conf import sender_email
from conf import app_password
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage

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


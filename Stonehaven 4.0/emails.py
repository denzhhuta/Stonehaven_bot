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
    html = f"""
        <html>
            <body>
                <p style="font-weight:bold;">Ваш код подтверждения: {confirmation_code}</p>
                <p style="font-size:12px;">С уважением, команда проекта Stonehaven.</p>
            </body>
        </html>
    """
    msg = EmailMessage()
    msg['Subject'] = 'Password Recovery'
    msg['From'] = sender_email
    msg['To'] = email
    msg.set_content(html, subtype='html')
    
    async with SMTP(hostname='smtp.gmail.com', port=587, start_tls=True,
                    username=sender_email, password=app_password) as smtp:
        await smtp.send_message(msg)
        
#Генерація рандомного коду
async def generate_confirmation_code() -> str:
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))

# async def send_email(subject, body, sender, recipients, password):
#     msg = EmailMessage()
#     msg['Subject'] = subject
#     msg['From'] = senders
#     msg['To'] = recipients
#     msg.set_content(body)

#     async with SMTP(hostname='smtp.gmail.com', port=587, start_tls=True,
#                     username=sender, password=password) as smtp:
#         await smtp.send_message(msg)
        
# asyncio.run(send_email('Test Email', 'This is a test email', sender_email, 'denis.zhhuta@gmail.com', app_password))
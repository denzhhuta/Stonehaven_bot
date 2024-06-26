from email.message import EmailMessage
from aiosmtplib import SMTP
import aiomysql
import random
import string
import asyncio
from conf import sender_email
from conf import app_password
#from main import confirmation_code
#from main import email

async def send_email(email: str, confirmation_code: str):
    msg = EmailMessage()
    msg['Subject'] = 'Password Recovery'
    msg['From'] = sender_email
    msg['To'] = email
    msg.set_content(f'Your confirmation code is: {confirmation_code}')

    async with SMTP(hostname='smtp.gmail.com', port=587, start_tls=True,
                    username=sender_email, password=app_password) as smtp:
        await smtp.send_message(msg)
        
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


async def generate_confirmation_code() -> str:
    #Генерація рандомного коду
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))


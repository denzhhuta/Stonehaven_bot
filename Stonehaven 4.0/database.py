import aiomysql
import aiogram
import asyncio
from datetime import datetime
from conf import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME


#функція коннекту до бази даних
async def connect_to_db():
    try:
        conn = await aiomysql.connect(
            host=DB_HOST,
            port=3306,
            user=DB_USER,
            password=DB_PASSWORD,
            db=DB_NAME,
            cursorclass=aiomysql.DictCursor)
    
        print("Connected successfully...")
        return conn
    
    except Exception as ex:
        print("Connection to DataBase refused...")
        print(ex)
        
#функція запиту з бази даних (інформація про гравця)
async def get_user_info(nickname):
    conn = await connect_to_db()
    async with conn.cursor() as cursor:
        #Якщо бещ COLLATE, то помилка
        #pymysql.err.OperationalError: (1267, "Illegal mix of collations 
        #(utf8mb3_general_ci,IMPLICIT) and (utf8mb4_general_ci,COERCIBLE) for operation '='")
        sql = "SELECT * FROM authme WHERE username=%s COLLATE utf8mb4_general_ci"
        #sql = "SELECT * FROM authme WHERE username=%s"
        await cursor.execute(sql, (nickname,))
        result = await cursor.fetchone()
    conn.close()

    STUCTURED_MESSAGE = """
        <b>Информация о пользователе:</b>
        <b>Ник: {username}</b>
        <b>IP адрес: {ip}</b>
        <b>Последний вход: {lastlogin}</b>
        <b>Дата регистрации: {regdate}</b>
        <b>Статус: {isLogged}</b>
        """

    if result:
        #dick, для isLogged
        logged_dict = {'0':'Оффлайн ❌', '1':'Онлайн ✅'}
        #перетворення часу, бо в бд з 1970 в мілісекундах
        timestamp_regdate = result['regdate'] / 1000
        regdate = datetime.fromtimestamp(timestamp_regdate)
        formatted_date_regdate = regdate.strftime("%Y-%m-%d %H:%M:%S")
        
        timestamp_lastlogin = result['lastlogin'] / 1000
        regdate_lastlogin = datetime.fromtimestamp(timestamp_lastlogin)
        formatted_date_lastlogin = regdate_lastlogin.strftime("%Y-%m-%d %H:%M:%S")
        #Dictionary, якщо 1 - Онлайн, 0 - Оффлайн, якщо немає співпадінь, то повертає пусту лінійку
        #тому пишемо ''
        is_logged_text = logged_dict.get(str(result['isLogged']), '')
        #форматуємо повідомлення 
        message_text = STUCTURED_MESSAGE.format(
            username=result['username'],
            realname=result['realname'],
            ip=result['ip'],
            lastlogin=formatted_date_lastlogin,
            regdate=formatted_date_regdate,
            isLogged=is_logged_text
            )
        return message_text
    else:
        return '<b>😔 Пользователь не найден. Пожалуйста, проверьте учетные данные!</b>'

#Перевірка чи емейл валідний.
async def is_valid_email(email):
    conn = await connect_to_db()
    async with conn.cursor() as cursor:
        sql = "SELECT * FROM authme WHERE email=%s COLLATE utf8mb4_general_ci"
        await cursor.execute(sql,(email,))
        result = await cursor.fetchone() 
    conn.close()
    
    if result:
        return True
    else:
        return False
    
#функція зміни паролю

async def new_password_db(hashed_password, email):
    try:
        conn = await connect_to_db()
        async with conn.cursor() as cursor:
            sql = "UPDATE authme SET password = %s WHERE email = %s"
            result = await cursor.execute(sql, (hashed_password, email))
            if result == 0:
                print(f"No rows were affected by the query for email {email}.")
            else:
                print(f"Password updated successfully for email {email}.")
                await logs_handler(email)
                #print(result)
            await conn.commit()  # add this line to commit changes
        conn.close()
    except Exception as e:
        print(f"An error occurred while updating the password for email {email}: {e}")
        
            
async def logs_handler(email, counter=[0]):
    counter[0] +=1
    try:
        with open('/Users/zgutadenis/Desktop/Stonehaven.project/Stonehaven_bot/Stonehaven 4.0/logs.txt', 'a') as f:
            f.write("\n{counter}.Password updated successfully for email {email} at {time}".format(counter=counter, email=email, time=datetime.now().strftime("%Y-%m-%d %H:%M")))
            
    except Exception as e:
            print(f"An error occurred while updating the password for email {email}: {e}")
            f.write("\n{counter}An error occurred while updating the password for email {email}: {exception} at {time}".format(counter=counter, email=email, exception=e, time=datetime.now().strftime("%Y-%m-%d %H:%M")))
    
# async def new_password_db(hashed_password, email):
#     try:
#         conn = await connect_to_db()
#         async with conn.cursor() as cursor:
#             now = datetime.datetime.now()
            
#             sql = "SELECT last_password_change FROM authme WHERE email = %s"
#             await cursor.execute(sql, (email,))
#             result = await cursor.fetchone()
#             last_password_change = result[0] if result else None
#             if last_password_change and now.date() == last_password_change.date():
#                 return await bot.send_message(chat_id=message.from_user.id, text="Нельзя менять пароль чаще чем 1 раз на день!</b>", parse_mode="HTML")
#             else:
#                 sql = "UPDATE authme SET password = %s WHERE email = %s"
#                 result = await cursor.execute(sql, (hashed_password, email))
#                 if result == 0:
#                     print(f"No rows were affected by the query for email {email}.")
#                 else:
#                  print(f"Password updated successfully for email {email}.")
#                 await conn.commit()  # Обов'язково зробити коміт, щоб зберегти запис в базу даних!
#         conn.close()
#     except Exception as e:
#         print(f"An error occurred while updating the password for email {email}: {e}")
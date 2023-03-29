import aiomysql
import aiogram
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
        return '<b>Пользователь не найден. Пожалуйста, проверьте учетные данные!</b>'

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
async def new_password(hashed_password, email):
    conn = await connect_to_db()
    async with conn.cursor() as cursor:
        sql = "UPDATE authme SET password =%s WHERE email=%s"
        await cursor.execute(sql, (hashed_password, email,))
    conn.close()
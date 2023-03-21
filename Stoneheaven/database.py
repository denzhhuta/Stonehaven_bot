import aiomysql
from conf import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME

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
        
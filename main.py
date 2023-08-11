from fastapi import FastAPI, UploadFile, Form, Response, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.staticfiles import StaticFiles
from fastapi_login import LoginManager
from fastapi_login.exceptions import InvalidCredentialsException
from typing import Annotated
import sqlite3

con = sqlite3.connect('db.db', check_same_thread=False)
cur = con.cursor()
# cur.execute(f"""
#                 CREATE TABLE IF NOT EXISTS items(
#                 id INTEGER PRIMARY KEY,
#                 title TEXT NOT NULL,
#                 image BLOB,
#                 price INTEGER NOT NULL,
#                 description TEXT,
#                 place TEXT NOT NULL,
#                 inserAt INTEGER NOT NULL
#                 );
#             """)

app = FastAPI()

# 로그인
SERCRET = "super-coding"
manager = LoginManager(SERCRET, '/login') #어디에서 발급되는지

@manager.user_loader()
def query_user(data):
    WHERE_STATEMENTS = f'id="{data}"'
    if type(data) == dict:
        WHERE_STATEMENTS = f'''id="{data["id"]}"'''
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    user = cur.execute(f"""
                        SELECT * FROM users WHERE {WHERE_STATEMENTS}
                       """).fetchone()
    return user


@app.post('/login')
def login(id:Annotated[str, Form()],
           password:Annotated[str, Form()]):
    user = query_user(id)
    if not user :
        raise InvalidCredentialsException #401에러 생성
    elif password != user['password']:
       raise InvalidCredentialsException
   
    access_token = manager.create_access_token(data={
        'sub':{
            'id' : user['id'],
            'name' : user['name'],
            'email' : user['email']
            }   
   })
   
    return {'access_token' : access_token} #res.status : 지정하지않아도 기본값 200으로 자동 return



@app.post('/signup')
def signup(id:Annotated[str, Form()],
           password:Annotated[str, Form()],
           name:Annotated[str, Form()],
           email:Annotated[str, Form()]):
    cur.execute(f"""
                INSERT INTO users(id, name, email, password) 
                VALUES ('{id}', '{name}', '{email}', '{password}')
                """)
    con.commit()
    
    print(id, password)
    return '200'


@app.post('/items')
async def create_items(image:UploadFile, 
                title:Annotated[str, Form()],
                price:Annotated[str, Form()], 
                description:Annotated[str, Form()], 
                place:Annotated[str, Form()],
                inserAt:Annotated[int, Form()]):
    
    image_bytes = await image.read()
    # 가져온 데이터를 SQL 테이블에 삽입
    cur.execute(f"""
                INSERT INTO items (title, image, price, description, place, inserAt)
                VALUES('{title}', '{image_bytes.hex()}', '{price}', '{description}', '{place}', '{inserAt}')
                """)
    con.commit()
    return '200'
    
@app.get('/items')
async def get_items(user=Depends(manager)): #유저가 인증된 사람만 depend(의존적) - token
    # 컬럼명도 같이 불러오도록 하는 코드
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    
    rows = cur.execute(f"""
                       SELECT * 
                       FROM items;
                       """).fetchall()
    return JSONResponse(jsonable_encoder((dict(row) for row in rows)))

# 이미지 응답 api
@app.get('/images/{item_id}')
async def get_image(item_id):
    cur = con.cursor()
    image_bytes=cur.execute(f"""
                            SELECT image
                            FROM items
                            WHERE id={item_id};
                            """).fetchone()[0]
    # 16진법을 2진변환
    return Response(content=bytes.fromhex(image_bytes))

app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")
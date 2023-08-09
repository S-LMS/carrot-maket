from fastapi import FastAPI, UploadFile, Form, Response
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.staticfiles import StaticFiles
from typing import Annotated
import sqlite3

con = sqlite3.connect('db.db', check_same_thread=False)
cur = con.cursor()

app = FastAPI()

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
async def get_items():
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
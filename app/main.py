from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth, lists
from app.database import Base, engine
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth, lists
from app.database import Base, engine
from app.routes import auth, places

# データベースの初期化
Base.metadata.create_all(bind=engine)

# main.py の create_all の直後に追加
import os
print("=== 現在のDBパス ===")
print(os.path.abspath(engine.url.database))

app = FastAPI()

# CORS の設定
origins = [
    "http://localhost",  # フロントエンドが動作しているドメイン
    "http://127.0.0.1:3000",  # 必要に応じて他のオリジンも追加
]

# CORS ミドルウェアの設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 必要に応じて特定のオリジンを指定
    allow_credentials=True,
    allow_methods=["*"],  # すべての HTTP メソッドを許可
    allow_headers=["*"],  # すべてのヘッダーを許可
)

# ルーターを追加
app.include_router(auth.router)
app.include_router(lists.router)
app.include_router(places.router)
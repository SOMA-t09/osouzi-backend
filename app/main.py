from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth, lists, places
from app.database import Base, engine

app = FastAPI()

# 起動時にDB初期化（import時にやらない）
@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth.router)
app.include_router(lists.router)
app.include_router(places.router)

@app.get("/")
def health():
    return {"ok": True}

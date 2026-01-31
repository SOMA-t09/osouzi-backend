from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth, lists, places
from app.database import Base, engine

app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(lists.router)
app.include_router(places.router)

@app.get("/")
def health():
    return {"ok": True}


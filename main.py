from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from sqlalchemy import select
from backend.app.db import Base, engine, SessionLocal
from backend.app.models import Intersection
from backend.app.api.routes import router

SEED = [
    ("Amir Temur - Navoi chorrahasi", 41.3111, 69.2797),
    ("Mustaqillik maydoni", 41.3126, 69.2928),
    ("Chilonzor - Bunyodkor chorrahasi", 41.2756, 69.2043),
]


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(engine)
    with SessionLocal() as db:
        if db.scalars(select(Intersection)).first() is None:
            db.add_all([Intersection(name=n, latitude=la, longitude=lo) for n, la, lo in SEED])
            db.commit()
    yield


app = FastAPI(title="Smart Traffic Management API", version="0.1.0", lifespan=lifespan)
app.include_router(router)


@app.get("/health")
def health():
    return {"status": "ok"}


frontend_dir = Path(__file__).resolve().parents[2] / "frontend"
if frontend_dir.exists():
    app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="frontend")

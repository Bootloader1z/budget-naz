from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.database import Base, engine
from app.routers import budget

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Budget-Naz")
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(budget.router)


@app.get("/")
def home():
    return FileResponse("app/templates/pages/budget.html")

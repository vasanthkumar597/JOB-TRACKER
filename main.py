from fastapi import FastAPI
from database import Base, engine
from routes import auth
from routes import user,jobs

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(jobs.router)
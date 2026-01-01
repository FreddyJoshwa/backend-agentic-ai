from fastapi import FastAPI
from app.routes import auth
from app.database import Base, engine
from app.routes import resume 

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(auth.router)
app.include_router(resume.router) 
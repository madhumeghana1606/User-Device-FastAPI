from fastapi import FastAPI
import models
from database import Base,engine
from sqlalchemy.orm import Session
from routers import user,device

app=FastAPI()


models.Base.metadata.create_all(engine)

app.include_router(user.router)
app.include_router(device.router)






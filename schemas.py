from typing import Optional,List
from datetime import datetime
from models import User,Device
from pydantic import BaseModel, ValidationError



class CreateDevice(BaseModel):
    type:str 
    active_status:bool
    user_id:int

class Model(CreateDevice):
    registered_time: datetime


    

class ShowDevice(CreateDevice):
    id:int 
    registered_time: datetime

    


class User(BaseModel):
    name:str
    email:str
    mobile_number:str
    device_id:int

class Show(User):
    id:int

class ShowUser(User):
    id:int
    user_registered_time:datetime


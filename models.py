from sqlalchemy import Column,Integer,String,Boolean,DateTime,ForeignKey,Table
from datetime import datetime
from database import Base
from sqlalchemy.orm import relationship


user_devices = Table('user_devices', Base.metadata,
    Column('device_id', ForeignKey('devices.id'), primary_key=True),
    Column('user_id', ForeignKey('users.id'), primary_key=True)
)

class Device(Base):
    __tablename__="devices"

    id=Column(Integer,primary_key=True,index=True)
    type=Column(String,nullable=False)
    active_status=Column(Boolean,default=True)
    registered_time=Column(DateTime,default=datetime.utcnow)
    user_id=Column(Integer,ForeignKey("users.id"))
    users=relationship("User",secondary="user_devices",back_populates="devices")

class User(Base):
    __tablename__="users"

    id=Column(Integer,primary_key=True,index=True)
    name=Column(String,nullable=False)
    email=Column(String)
    mobile_number=Column(String(10))
    user_registered_time=Column(DateTime,default=datetime.now())
    device_id=Column(Integer,ForeignKey("devices.id"))

    devices=relationship("Device",secondary="user_devices",back_populates="users")




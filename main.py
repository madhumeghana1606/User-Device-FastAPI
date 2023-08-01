from fastapi import FastAPI,Depends,HTTPException
import schemas,models
from database import Base,engine,get_db
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime


app=FastAPI()


models.Base.metadata.create_all(engine)
@app.post('/device',response_model=schemas.ShowDevice,tags=["device"])
def create_device(request:schemas.Model,db:Session=Depends(get_db)):
    new_device=models.Device(type=request.type,active_status=request.active_status,user_id=request.user_id,registered_time=request.registered_time)
    db.add(new_device)
    db.commit()
    db.refresh(new_device)
    return new_device

@app.get('/device/{user_id}',response_model=List[schemas.ShowDevice],tags=["device"])
def get_devices_of_specific_user(user_id,db:Session=Depends(get_db)):
    users=db.query(models.Device).filter(models.Device.user_id==user_id).all()
    return users

@app.get('/device',response_model=List[schemas.ShowDevice],tags=["device"])
def get_all(db:Session=Depends(get_db)):
    devices=db.query(models.Device).all()
    return devices


@app.get('/device/{id}',response_model=schemas.ShowDevice,tags=["device"])
def show_device(id,db:Session=Depends(get_db)):
    device=db.query(models.Device).filter(models.Device.id==id).first()
    if not device:
        raise HTTPException(status_code=404,detail="device with this id is not found")
    return device



@app.delete('/device/{id}',tags=["device"])
def destroy(id,db:Session=Depends(get_db)):
    device=db.query(models.Device).filter(models.Device.id==id).delete(synchronize_session=False)
    if not device:
        raise HTTPException(status_code=404,detail="device with this id is not found")
    db.commit()
    return "Suceessfully deleted"

@app.put('/device/{id}',tags=["device"])
def update(id,request:schemas.CreateDevice,db:Session=Depends(get_db)):
    new_device=db.query(models.Device).filter(models.Device.id==id).update(request.dict())
    if not new_device:
        raise HTTPException(status_code=404,detail="device with this id is not found")
    db.commit()
    return "Suceessfully updated"








@app.post('/user',response_model=schemas.Show,tags=["user"])
def create_user(request:schemas.User,db:Session=Depends(get_db)):
    user=models.User(name=request.name,email=request.email,mobile_number=request.mobile_number,device_id=request.device_id)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@app.get('/user/{device_id}',response_model=List[schemas.ShowUser],tags=["user"])
def get_users_for_specific_device(device_id,db:Session=Depends(get_db)):
    devices=db.query(models.User).filter(models.User.device_id==device_id).all()
    return devices


@app.get('/user',response_model=List[schemas.ShowUser],tags=["user"])
def get_all_users(db:Session=Depends(get_db)):
    users=db.query(models.User).all()
    db.commit()
    return users

@app.get('/user/{id}',response_model=schemas.ShowUser,tags=["user"])
def get_user(id,db:Session=Depends(get_db)):
    user=db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code=404,detail="User not found")
    db.commit()
    return user
@app.put('/user/{id}',tags=["user"])
def update_user(id,request:schemas.User,db:Session=Depends(get_db)):
    user=db.query(models.User).filter(models.User.id==id).update(request.dict())
    if not user:
        raise HTTPException(status_code=404,detail="User not found")
    db.commit()
    return "Successfullly updated"

@app.delete('/user/{id}',tags=["user"])
def destroy_user(id,db:Session=Depends(get_db)):
    user=db.query(models.User).filter(models.User.id==id).delete(synchronize_session=False)
    db.commit()
    return "Suceessfully deleted"
from fastapi import APIRouter,Depends,HTTPException,Query
import schemas,models
from typing import List
from database import get_db
from sqlalchemy import func
from sqlalchemy.orm import Session

router=APIRouter(
    tags=['Tasks'],
    prefix="/userdevice"
)

@router.get('/count_registered')
def count_registered_devices(month: int = Query(..., description="Month (1-12)"),db:Session=Depends(get_db)):
    if month<1 or month>12:
        raise HTTPException(status_code=400,detail="Invalid Month")
    device_count=db.query(models.Device).filter(func.extract('month',models.Device.registered_time) == month).count()
    db.close()
    return {"devices_count":device_count}


@router.get('/getdevice/{device_id}',response_model=List[schemas.ShowUser])
def get_users_for_specific_device(device_id,db:Session=Depends(get_db)):
    devices=db.query(models.User).filter(models.User.device_id==device_id).all()
    return devices

@router.get('/getuser/{user_id}',response_model=List[schemas.ShowDevice])
def get_devices_of_specific_user(user_id,db:Session=Depends(get_db)):
    users=db.query(models.Device).filter(models.Device.user_id==user_id).all()
    return users

@router.get('/device_with_more_users')
def get_device_with_highest_users(db:Session=Depends(get_db)):
    subquery = db.query(models.User.device_id, func.count(models.User.id).label("user_count")).group_by(models.User.device_id).subquery()
    result = db.query(models.Device, subquery.c.user_count).join(subquery, models.Device.id == subquery.c.device_id).order_by(subquery.c.user_count.desc()).first()
    db.close()

    if result:
        devices, user_count = result
        return {
            "device_id": devices.id,
            "device_name": devices.type,
            "user_count": user_count
        }
    else:
        raise HTTPException(status_code=404, detail="No devices found")
    
@router.get('/total_active_device')
def get_total_active_device(db:Session=Depends(get_db)):
    active_status_count=db.query(models.Device).filter(models.Device.active_status==True).count()
    db.close()
    return {"active_status_count":active_status_count}
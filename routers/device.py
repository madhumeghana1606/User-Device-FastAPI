from fastapi import APIRouter,Depends,HTTPException,Query
import schemas,models
from typing import List
from database import get_db
from sqlalchemy import func
from sqlalchemy.orm import Session

router=APIRouter(
    tags=['device'],
    prefix="/device"
)

    

@router.get('',response_model=List[schemas.ShowDevice])
def get_all(db:Session=Depends(get_db)):
    devices=db.query(models.Device).all()
    return devices

@router.post('',response_model=schemas.ShowDevice)
def create_device(request:schemas.Model,db:Session=Depends(get_db)):
    new_device=models.Device(type=request.type,active_status=request.active_status,user_id=request.user_id,registered_time=request.registered_time)
    db.add(new_device)
    db.commit()
    db.refresh(new_device)
    return new_device


@router.get('/{id}',response_model=schemas.ShowDevice)
def show_device(id,db:Session=Depends(get_db)):
    device=db.query(models.Device).filter(models.Device.id==id).first()
    if not device:
        raise HTTPException(status_code=404,detail="device with this id is not found")
    return device




@router.delete('/{id}')
def destroy(id,db:Session=Depends(get_db)):
    device=db.query(models.Device).filter(models.Device.id==id).delete(synchronize_session=False)
    if not device:
        raise HTTPException(status_code=404,detail="device with this id is not found")
    db.commit()
    return "Suceessfully deleted"

@router.put('/{id}')
def update(id,request:schemas.CreateDevice,db:Session=Depends(get_db)):
    new_device=db.query(models.Device).filter(models.Device.id==id).update(request.dict())
    if not new_device:
        raise HTTPException(status_code=404,detail="device with this id is not found")
    db.commit()
    return "Suceessfully updated"


from fastapi import APIRouter,Depends,HTTPException
import schemas,models
from typing import List
from database import get_db
from sqlalchemy.orm import Session

router=APIRouter(
    tags=['user'],
    prefix="/user"
)



@router.post('',response_model=schemas.Show)
def create_user(request:schemas.User,db:Session=Depends(get_db)):
    user=models.User(name=request.name,email=request.email,mobile_number=request.mobile_number,device_id=request.device_id)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.get('/getdevice/{device_id}',response_model=List[schemas.ShowUser])
def get_users_for_specific_device(device_id,db:Session=Depends(get_db)):
    devices=db.query(models.User).filter(models.User.device_id==device_id).all()
    return devices


@router.get('',response_model=List[schemas.ShowUser])
def get_all_users(db:Session=Depends(get_db)):
    users=db.query(models.User).all()
    db.commit()
    return users

@router.get('/device/{id}',response_model=schemas.ShowUser)
def get_user(id,db:Session=Depends(get_db)):
    user=db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code=404,detail="User not found")
    db.commit()
    return user


@router.put('/{id}')
def update_user(id,request:schemas.User,db:Session=Depends(get_db)):
    user=db.query(models.User).filter(models.User.id==id).update(request.dict())
    if not user:
        raise HTTPException(status_code=404,detail="User not found")
    db.commit()
    return "Successfullly updated"

@router.delete('/{id}')
def destroy_user(id,db:Session=Depends(get_db)):
    user=db.query(models.User).filter(models.User.id==id).delete(synchronize_session=False)
    db.commit()
    return "Suceessfully deleted"
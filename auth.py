#Register and Login logic
#Register user = save to mysql
#login user = (verify + redirect )
from fastapi import HTTPException,Depends
from fastapi import status
from sqlalchemy.orm import Session
from passlib.context import CryptContext

#from . import models,schemas,database
import models
import schemas
import database

#password hashing utility using bcrypt
pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")

#Hash a plain password
def hash_password(password:str) -> str :
    return pwd_context.hash(password)

#verify password against its hash
def verify_password(plain_password:str,hashed_password:str) -> bool:  # compares plain and hashed password
    return pwd_context.verify(plain_password,hashed_password)

#=========================================================================================================================
#Register a new user
def register_user(user_data:schemas.UserCreate,db:Session):#register user if email not exist
    existing_user = db.query(models.User).filter(models.User.email==user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Email already registered")

    hashed_pwd=hash_password(user_data.password)
    new_user=models.User(name=user_data.name,email=user_data.email,password_hash=hashed_pwd)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
#======================================================================================================================
#Login an existing user
def login_user(user_data:schemas.UserLogin,db:Session):# logs in user if credentials are valid
    user=db.query(models.User).filter(models.User.email==user_data.email).first()
    if not user or not verify_password(user_data.password,user.password_hash):
        raise HTTPException(status_code=401,detail="Invalid Credentials")
        return user
#=====================================================================================================
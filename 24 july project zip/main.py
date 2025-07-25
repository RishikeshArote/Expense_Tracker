from fastapi import FastAPI,Request,Depends,Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from models import User

import models,schemas,auth
from database import SessionLocal,engine,Base
import database
#=======================================================================================================================
# Create tables
models.Base.metadata.create_all(bind=engine)
#=======================================================================================================================

#initialize fastapi
app = FastAPI()
#=======================================================================================================================

#create database tables on startup
Base.metadata.create_all(bind=engine)
#====================================================================================================================

#mount templates and static folders
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"),name="static")
#====================================================================================================================

#create database tables on startup
models.Base.metadata.create_all(bind=database.engine)
#Dependancy to get DB session
def get_db():
    db=database.SessionLocal()
    try:
        yield db
    finally:
        db.close()
#=====================================================================================================================
#home page
@app.get("/",response_class=HTMLResponse)
def home(request:Request):
    return templates.TemplateResponse("login.html",{"request":request})
#=======================================================================================================================
#register page(GET)
@app.get("/register",response_class=HTMLResponse)
def register_page(request:Request):
    return templates.TemplateResponse("register.html",{"request":request})
#======================================================================================================================
#Register Handler(POST)
@app.post("/register",response_class=HTMLResponse)
def register_user(request:Request,name:str=Form(...),email:str=Form(...),password:str=Form(...),db:Session=Depends(get_db)):
    print(password,name,email,'etdegtdyerytrdgtydgetdytdyedt')
    user_data=schemas.UserCreate(name=name,email=email,password=password)
    print(user_data,'frsdexzedxasxwedw')
    user=User(username=name,email=email,password=password)
    print(user,"hiiiiiiiiiiiii")
    db.add(user)
    db.commit()  # <— This is usually required to persist changes
   
    # return RedirectResponse(url="/login", status_code=303)
    return templates.TemplateResponse("login.html",{
                "request":request,
            }) 


#======================================================================================================================
#Login Handler (Post)
@app.post("/login",response_class=HTMLResponse)
def login_user(request:Request,email:str=Form(...),password:str=Form(...),db:Session=Depends(get_db)):
    user_data=schemas.UserLogin(email=email,password=password)
    print(email,password,'sucessfully login')
    # return "Hello "
    # try:
    #     user=auth.login_user(user_data,db)
    #     return templates.TemplateResponse("home.html",{"request":request,"message":f"WELCOME!"})
    
    # except Exception as e:
    return templates.TemplateResponse("home.html",{"request":request})
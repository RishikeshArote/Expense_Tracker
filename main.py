from fastapi import FastAPI,Request,Depends,Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import bcrypt
from sqlalchemy.orm import Session
from models import User

import models,schemas,auth
from database import SessionLocal,engine,Base
import database
#====================================================================================================================
# Create tables
models.Base.metadata.create_all(bind=engine)
#====================================================================================================================
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
def register_user(
                    request:Request,
                    name     : str     = Form(...),
                    email    : str     = Form(...),
                    password : str     = Form(...),
                    db       : Session = Depends(get_db)
                 ):
    # Check if email is already registered
    existing_user = db.query(User).filter(User.email == email).first()

    if existing_user:
        return templates.TemplateResponse("register.html", {
                                                            "request": request,
                                                            "error": "Email already registered. Please log in or use a different one",
                                                            "name": name,
                                                            "email": email
                                                            })


    # Hash the password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Store the hashed password
    user = User(username=name, email=email, password=hashed_password.decode('utf-8'))
   
    db.add(user)
    db.commit()
    db.refresh(user)

    return templates.TemplateResponse("login.html", {"request": request})
#======================================================================================================================
#Login Handler (Post)
@app.post("/login",response_class=HTMLResponse)
def login_user(
                request:Request,
                email    : str     = Form(...),
                password : str     = Form(...),
                db       : Session = Depends(get_db)
               ):
    user = db.query(User).filter(User.email == email).first()
    
    if not user or not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        return templates.TemplateResponse("login.html", { "request": request,
                                                          "error": " Invalid email or password"
                                                        } )
   
    return templates.TemplateResponse("dashboard.html",{"request":request})
#======================================================================================================================

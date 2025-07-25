from pydantic import BaseModel,EmailStr,Field
#========================================================================================================================
#schema for user registratin input
class UserCreate(BaseModel):
    name:str       = Field(...,example="Rishikesh Arote")
    email:EmailStr = Field(...,example="rishiarote2020@gmail")
    password:str   = Field(...,example="rishikesh")
#========================================================================================================================
#schema for user login input
class UserLogin(BaseModel):
    email:EmailStr = Field(...,example="rishiarote2020@gmail.com")
    password:str   = Field(...,example="rishikesh")
#========================================================================================================================
#schema for showing user data(response model)
class UserResponse(BaseModel):
    id:int
    name:str
    email:EmailStr
    
    class Config:
        from_attributes = True   #enables reading from SQLAchemy model
#========================================================================================================================

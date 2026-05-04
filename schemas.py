from pydantic import BaseModel

class UserSchema(BaseModel):
    name: str
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: str

class JobCreate(BaseModel):
    title:str
    company:str
    status:str
    salary:str|None=None

class JobResponse(BaseModel):
    id:int
    title:str
    company:str
    status:str
    

    class Config:
        from_attributes=True
        
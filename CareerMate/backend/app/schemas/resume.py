from pydantic import BaseModel

class ResumeCreate(BaseModel):
    goals: str

class ResumeUpdate(BaseModel):
    skills: str
    goals: str

class ResumeOut(BaseModel):
    id: int
    user_id: int
    skills: str
    goals: str

    class Config:
        orm_mode = True

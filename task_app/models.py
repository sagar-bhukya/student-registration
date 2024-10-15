from pydantic import BaseModel
from datetime import datetime

class Student(BaseModel):
    first_name: str
    last_name: str
    qualification:str
    email:str
    mobile:str
    course:str
    date_of_Registration: datetime
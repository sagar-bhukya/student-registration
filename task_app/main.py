from fastapi import FastAPI,Form,Request
from pymongo import MongoClient
from pydantic import BaseModel
from datetime import datetime
from database import collection
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app=FastAPI()

templates=Jinja2Templates(directory="templates")

@app.get('/',response_class=HTMLResponse)
def registration_form(request:Request):
    return templates.TemplateResponse("home.html",{"request":request})

@app.post('/register') #for student register
def register_student(first_name: str=Form(...),last_name: str=Form(...),qualification:str=Form(...),email:str=Form(...),mobile:str=Form(...),course:str=Form(...)):
    registration_data={
    "first_name": first_name,
    "last_name": last_name,
    "qualification":qualification,
    "email":email,
    "mobile":mobile,
    "course":course,
    "date_of_Registration": datetime.now()
    }
    inserted=collection.insert_one(registration_data)
        # Add the inserted ID to the response
    registration_data["_id"] = str(inserted.inserted_id)
    
    return {"message": "student data Done", "data": registration_data}


#endpoint for Year wise Registrations
@app.get("/reports/yearwise-registrations")
def yearwise_registrations():
    pipeline=[
        {
            "$group":{
                "_id":{"$year":"$date_of_Registration"},
                "count":{"$sum":1}
            }
        }
    ]
    result=list(collection.aggregate(pipeline))

    return result

#endpoint for Course wise Trends in a given year
@app.get("/reports/coursewise-trends/{year}")
def courswise_trends(year:int):
    pipeline=[
        {"$match":{"$expr":{"$eq":[{"$year":"$date_of_Registration"},year]}}},
        {"$group":{
            "_id":"$course",
            "count":{"$sum":1}
        }}
    ]

    result=list(collection.aggregate(pipeline))
    return result
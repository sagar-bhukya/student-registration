from pymongo import MongoClient

mongodb=MongoClient("mongodb://localhost:27017/")
db=mongodb.sagar
collection=db.registrations
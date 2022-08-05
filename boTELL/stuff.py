from pymongo import MongoClient
from datetime import date
from pymongo.errors import DuplicateKeyError

client = MongoClient("mongodb+srv://bottell_0:9B89MhM9OY3u61j6@cluster0.jwwlt.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client.get_database("bottell_db")

student_record = db.Students
fac_record = db.Faculty

def search():
    cursor = student_record.find({'DOB': '11 12 2001'}) #{'DOB': dob}
    for doc in cursor:
        lol = doc['Pending_assigns']
        break
    print(list(lol.keys()))


search()
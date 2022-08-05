from pymongo import MongoClient
from datetime import date
from pymongo.errors import DuplicateKeyError


LINK = 'mongodb+srv://bottell_0:9B89MhM9OY3u61j6@cluster0.jwwlt.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'
client = MongoClient(LINK)
db = client.get_database("bottell_db")

student_record = db.Students
fac_record = db.Faculty

today = date.today()
today_str = str(today)

date_ = today_str[5:10] #8:10 #month_ = today_str[5:7]
present_year_int = int(today_str[:4])

#User-defined functions

#insert one by one values
def insert_(name, ID, dept, dob, mail, user_id, record):
    # dm = dob[5:10]
    _date_ = str(dob.split()[0]) + " " + str(dob.split()[1])
    record.create_index('ID', unique = True) #create index(to avoid duplicate entries)
    to_insert = {
        'UID': user_id,
        'Name': name,
        'ID': ID,
        'Dept': dept,
        'DOB': dob,
        'Date': _date_,
        'Mail': mail
    }
    if record == student_record:
        to_insert.update({'Pending_assigns': {}})
    record.insert_one(to_insert) #insert_many

'''
#insert many values at a time
def insert_more(record, name, roll_no, dept, dob, value_lst):
    record.create_index('Roll_no', unique = True) #create index(to avoid duplicate entries)
    record.insert_many(value_lst)
'''

#update values
def update_record(name, ID, dept, dob, mail, record):
    student_update = {
        'Name': name,
        'Dept': dept,
        'DOB': dob,
        'Date': str(dob.split()[0]) + " " + str(dob.split()[1]),
        'Mail': mail
    }
    record.update_one({'ID': ID}, {'$set': student_update})


def add_assign(assign_id, assigner):
    assigner = str(assigner)
    assign_id = str(assign_id)
    # student_update = {
    #     'Pending_assigns': {assigner: assign_id}
    # }
    student_record.update_many({}, {'$set': {f'Pending_assigns.{assign_id}': assigner}})
    # student_record.aggregate([{'$addFields': {f'Pending_assigns.{assigner}': assign_id}}])


def del_assign(assign_id, student_id):
    student_record.update({'UID': student_id}, {'$unset': {f'Pending_assigns.{assign_id}': None}})


def find_assigner(assign_id, student_id):
    cursor = student_record.find({'UID': student_id})  # {'DOB': dob}
    for doc in cursor:
        return doc['Pending_assigns'][assign_id]


def pending_assigns(student_id):
    cursor = student_record.find({'UID': student_id})
    for doc in cursor:
        lol = doc['Pending_assigns']
        break
    return list(lol.keys())



#delete account
def delete_accnt(record, ID):
    record.delete_one({'ID': ID})


#count num of records
def count_by_id(record, id):
    cnt = record.count_documents({'ID': id}) #count for cse only
    return cnt


def count_by_uid(record, uid):
    cnt = record.count_documents({'UID': uid}) #count for cse only
    return cnt


#find doc
def search(record, dob):
    cursor = record.find({'DOB': dob}) #{'DOB': dob}
    for doc in cursor:
        print(doc)


def exists(ID, record):
    cursor = record.find({'ID': ID})
    return len(cursor)


from pymongo import MongoClient

client = MongoClient("mongodb+srv://Vishal:*password*.@firstcluster.dhxrvm7.mongodb.net/")
db = client.get_database("ExpenseDB")
user_collection = db["users"]
group_collection = db["groups"]
expense_collection = db["expenses"]
owes_collection = db["owes"]


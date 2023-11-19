
# Welcome to Expense Sharing App!

This is an Expense Sharing App that lets the user share expense among group participants. 

Technologies used for creating the App:
* Python's FastAPI
* Mongo DB

## DB Schema
![DB Schema.jpg](DB%20Schema.jpg)

## Mongo DB 
The application uses MongoDB as the Database to store and retrieve values.

### Set up
Go to https://account.mongodb.com/ and create an account.
After creation of account go to  https://www.mongodb.com/products/tools/compass and download MongoDB compass.

After creating an account on mongoDB and making a Database , you will get a cluster link copy and paste the cluster link in DB compass and connect to the cluster.
 
Your Database connection is established.

# Python

Packages required  for the project.
* FastAPI
* Pymongo 
* uvicorn[standard] 

To install the required packages run the below command:-
```
pip install -r requirement.txt
``` 

In the Expense there are 3 sub folder (4th one being venv(virtual environment)).
*Config contains our DB connection.
*Models contains the schema's.
*Routes contain the respective Routes
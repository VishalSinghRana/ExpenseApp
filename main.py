from fastapi import FastAPI
from routes.expense import expense_app


app = FastAPI()
app.include_router(expense_app)




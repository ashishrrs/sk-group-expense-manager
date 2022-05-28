from fastapi import FastAPI
from routers import expensetracker
app = FastAPI()

app.include_router(expensetracker.router)

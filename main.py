from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import sqlalchemy as sa
import pandas as pd

from routers import customers, dvds, employees, rentals

# app initialization
app = FastAPI()
# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# routers
app.include_router(customers.router)
app.include_router(dvds.router)
app.include_router(employees.router)
app.include_router(rentals.router)

# auth endpoint
@app.get("/auth/")
def get_user(username: str, password: str):
    query = sa.text(f"SELECT * FROM employees WHERE username='{username}' AND password='{password}'")
    engine = sa.create_engine("sqlite:///db/bcr.db")
    try:
        employee = pd.read_sql(query, engine).to_dict(orient='records')[0]
    except:
        raise HTTPException(404, "Employee not found.")
    return employee
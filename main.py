from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import customers, dvds, employees, rentals

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(customers.router)
app.include_router(dvds.router)
app.include_router(employees.router)
app.include_router(rentals.router)

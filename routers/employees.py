from fastapi import APIRouter, HTTPException
import pandas as pd
import sqlalchemy as sa
from pydantic import BaseModel

router = APIRouter(
    prefix="/employees",
    tags=["employees"],
    responses={404: {"description": "Not found."}}
)


@router.get("/")
def get_employees():
    query = sa.text("SELECT * FROM employees")
    engine = sa.create_engine("sqlite:///db/bcr.db")
    employees = pd.read_sql(query, engine)
    return employees.to_dict(orient='records')


class Employee(BaseModel):
    id: int | None = None
    name: str
    address: str
    rentals: int | None = None
    username: str
    password: str


@router.post("/")
def create_employee(employee: Employee):
    query = sa.text(f"""
        INSERT INTO employees
        (name, address, rentals, username, password)
        VALUES
        ('{employee.name}','{employee.address}',0,'{employee.username}','{employee.password}')
    """)
    engine = sa.create_engine("sqlite:///db/bcr.db")
    connection = engine.connect()
    try:
        connection.execute(query)
        connection.commit()
    except Exception as e:
        connection.close()
        print(e)
        raise HTTPException(500, "Database Error")
    connection.close()
    return {"message": "success"}


@router.put("/")
def update_employee(employee: Employee):
    if not employee.id:
        raise HTTPException(422, "Bad request: Employee ID is required.")
    query = sa.text(f"""
        UPDATE employees SET
            name = '{employee.name}',
            address = '{employee.address}',
            rentals = {employee.rentals},
            username = '{employee.username}',
            password = '{employee.password}'
        WHERE id = {employee.id}
    """)
    engine = sa.create_engine("sqlite:///db/bcr.db")
    connection = engine.connect()
    try:
        connection.execute(query)
        connection.commit()
    except Exception as e:
        connection.close()
        print(e)
        raise HTTPException(500, "Database Error")
    connection.close()
    return {"message": "success"}


@router.delete("/{employee_id}")
def delete_employee(employee_id: int):
    query = sa.text(f"DELETE FROM employees WHERE id = {employee_id}")
    engine = sa.create_engine("sqlite:///db/bcr.db")
    connection = engine.connect()
    try:
        connection.execute(query)
        connection.commit()
    except Exception as e:
        connection.close()
        print(e)
        raise HTTPException(500, "Database Error")
    connection.close()
    return {"message": "success"}

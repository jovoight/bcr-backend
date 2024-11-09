from fastapi import APIRouter, HTTPException
import pandas as pd
import sqlalchemy as sa
from pydantic import BaseModel

router = APIRouter(
    prefix="/customers",
    tags=["customers"],
    responses={404: {"description": "Not found."}}
)


@router.get("/")
def get_customers():
    query = sa.text("SELECT * FROM customers")
    engine = sa.create_engine("sqlite:///db/bcr.db")
    customers = pd.read_sql(query, engine)
    return customers.to_dict(orient='records')


class Customer(BaseModel):
    id: int | None = None
    name: str
    address: str
    late_fees: float | None = None


@router.post("/")
def create_customer(customer: Customer):
    query = sa.text(f"""
        INSERT INTO customers
        (name, address, late_fees)
        VALUES
        ('{customer.name}','{customer.address}',0)
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
def update_customer(customer: Customer):
    if not customer.id:
        raise HTTPException(422, "Bad request: Customer ID is required.")
    query = sa.text(f"""
        UPDATE customers SET
            name = '{customer.name}',
            address = '{customer.address}',
            late_fees = {customer.late_fees}
        WHERE id = {customer.id}
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


@router.delete("/{customer_id}")
def delete_customer(customer_id: int):
    query = sa.text(f"DELETE FROM customers WHERE id = {customer_id}")
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

from fastapi import APIRouter, HTTPException
import pandas as pd
import sqlalchemy as sa
from pydantic import BaseModel

router = APIRouter(
    prefix="/rentals",
    tags=["rentals"],
    responses={404: {"description": "Not found."}}
)


@router.get("/")
def get_rentals():
    query = sa.text("SELECT * FROM rentals")
    engine = sa.create_engine("sqlite:///db/bcr.db")
    rentals = pd.read_sql(query, engine)
    return rentals.to_dict(orient='records')


class Rental(BaseModel):
    id: int | None = None
    customer_id: int
    dvd_id: int
    employee_id: int
    payment_method: str
    payment_amount: float
    rent_date: str
    due_date: str
    return_date: str | None = None


@router.post("/")
def create_rental(rental: Rental):
    query = sa.text(f"""
        INSERT INTO rentals (
            customer_id,
            dvd_id,
            employee_id,
            payment_method,
            payment_amount,
            rent_date,
            due_date
        )
        VALUES (
            {rental.customer_id},
            {rental.dvd_id},
            {rental.employee_id},
            '{rental.payment_method}',
            {rental.payment_amount},
            '{rental.rent_date}',
            '{rental.due_date}'
        )
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
def update_rental(rental: Rental):
    if not rental.id:
        raise HTTPException(422, "Bad request: Rental ID is required.")
    query = sa.text(f"""
        UPDATE rentals SET
            customer_id = {rental.customer_id},
            dvd_id = {rental.dvd_id},
            employee_id = {rental.employee_id},
            payment_method = '{rental.payment_method}',
            payment_amount = {rental.payment_amount},
            rent_date = '{rental.rent_date}',
            due_date = '{rental.due_date}',
            return_date = '{rental.return_date}'
        WHERE id = {rental.id}
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


@router.delete("/{rental_id}")
def delete_rental(rental_id: int):
    query = sa.text(f"DELETE FROM rentals WHERE id = {rental_id}")
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

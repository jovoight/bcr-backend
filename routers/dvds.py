from fastapi import APIRouter, HTTPException
import pandas as pd
import sqlalchemy as sa
from pydantic import BaseModel

router = APIRouter(
    prefix="/dvds",
    tags=["dvds"],
    responses={404: {"description": "Not found."}}
)


@router.get("/")
def get_dvds():
    query = sa.text("SELECT * FROM dvds")
    engine = sa.create_engine("sqlite:///bcr.db")
    dvds = pd.read_sql(query, engine)
    return dvds.to_dict(orient='records')


class Dvd(BaseModel):
    id: int | None = None
    name: str
    status: str
    img: str
    description: str
    genre: str
    rental_category: str


@router.post("/")
def create_dvd(dvd: Dvd):
    query = sa.text(f"""
        INSERT INTO dvds
        (name, status, img, description, genre, rental_category)
        VALUES
        ('{dvd.name}','{dvd.status}','{dvd.img}','{dvd.description}','{dvd.genre}','{dvd.rental_category}')
    """)
    engine = sa.create_engine("sqlite:///bcr.db")
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
def update_dvd(dvd: Dvd):
    if not dvd.id:
        raise HTTPException(422, "Bad request: DVD ID is required.")
    query = sa.text(f"""
        UPDATE dvds SET
            name = '{dvd.name}',
            status = '{dvd.status}',
            img = '{dvd.img}',
            description = '{dvd.description}',
            genre = '{dvd.genre}',
            rental_category = '{dvd.rental_category}'
        WHERE id = {dvd.id}
    """)
    engine = sa.create_engine("sqlite:///bcr.db")
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


@router.delete("/{dvd_id}")
def delete_dvd(dvd_id: int):
    query = sa.text(f"DELETE FROM dvds WHERE id = {dvd_id}")
    engine = sa.create_engine("sqlite:///bcr.db")
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

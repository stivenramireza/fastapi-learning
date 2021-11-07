# Python
from typing import Dict, Optional
from enum import Enum

# Pydantic
from pydantic import BaseModel, Field

# FastAPI
from fastapi import FastAPI, Body, Query, Path, status


app = FastAPI()


# Models
class HairColor(Enum):
    WHITE: "WHITE"
    BROWN = "BROWN"
    BLACK = "BLACK"
    BLONDE = "BLONDE"
    RED = "RED"


class PersonBase(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=50, example="Stiven")
    last_name: str = Field(..., min_length=1, max_length=50, example="Ramírez Arango")
    age: int = Field(..., gt=0, le=115, example=23)
    hair_color: Optional[HairColor] = Field(default=None, example="BLACK")
    is_married: Optional[bool] = Field(default=None, example=False)


class Person(PersonBase):
    password: str = Field(..., min_length=8, example="password")


class PersonOut(PersonBase):
    pass


class Location(PersonBase):
    city: str = Field(..., min_length=1, max_length=50, example="Sabaneta")
    state: str = Field(..., min_length=1, max_length=50, example="Antioquia")
    country: str = Field(..., min_length=1, max_length=50, example="Colombia")


@app.get(path="/", status_code=status.HTTP_200_OK)
def home() -> Dict[str, any]:
    return {"Hello": "World"}


# Request and Response Body
@app.post(
    path="/person/new", response_model=PersonOut, status_code=status.HTTP_201_CREATED
)
def create_person(person: Person = Body(...)) -> Dict[str, any]:
    return person


# Validations: Query Parameters
@app.get("/person/detail", status_code=status.HTTP_200_OK)
def show_person(
    name: Optional[str] = Query(
        default=None,
        min_length=1,
        max_length=50,
        title="Person name",
        description="This is the person name. It's between 1 and 50 characters",
        example="Stiven",
    ),
    age: int = Query(
        ...,
        title="Person age",
        description="This is the person age. It's required",
        example=23,
    ),
) -> Dict[str, any]:
    return {name: age}


# Validations: Path Parameters
@app.get("/person/detail/{person_id}", status_code=status.HTTP_200_OK)
def show_person(
    person_id: int = Path(
        ...,
        gt=0,
        title="Person id",
        description="This is the person id. It's required",
        example=123,
    )
) -> Dict[str, any]:
    return {person_id: "It exists!"}


# Validations: Request Body
@app.put("/person/{person_id}", status_code=status.HTTP_204_NO_CONTENT)
def update_person(
    person_id: int = Path(
        ..., title="Person id", description="This is the person id", gt=0, example=123
    ),
    person: Person = Body(...),
    location: Location = Body(...),
):
    return {**dict(person), **dict(location)}

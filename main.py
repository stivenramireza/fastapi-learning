# Python
from typing import Dict, Optional
from enum import Enum

# Pydantic
from pydantic import BaseModel, Field

# FastAPI
from fastapi import FastAPI, Body, Query, Path


app = FastAPI()


# Models
class HairColor(Enum):
    WHITE: "WHITE"
    BROWN = "BROWN"
    BLACK = "BLACK"
    BLONDE = "BLONDE"
    RED = "RED"


class Person(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=50, example="Stiven")
    last_name: str = Field(..., min_length=1, max_length=50, example="Ramírez Arango")
    age: int = Field(..., gt=0, le=115, example=23)
    hair_color: Optional[HairColor] = Field(default=None, example="BLACK")
    is_married: Optional[bool] = Field(default=None, example=False)
    password: str = Field(..., min_length=8)


class Location(BaseModel):
    city: str = Field(..., min_length=1, max_length=50, example="Sabaneta")
    state: str = Field(..., min_length=1, max_length=50, example="Antioquia")
    country: str = Field(..., min_length=1, max_length=50, example="Colombia")


@app.get("/")
def home() -> Dict[str, any]:
    return {"Hello": "World"}


# Request and Response Body
@app.post("/person/new", response_model=Person, response_model_exclude={"password"})
def create_person(person: Person = Body(...)) -> Dict[str, any]:
    return person


# Validations: Query Parameters
@app.get("/person/detail")
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
@app.get("/person/detail/{person_id}")
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
@app.put("/person/{person_id}")
def update_person(
    person_id: int = Path(
        ..., title="Person id", description="This is the person id", gt=0, example=123
    ),
    person: Person = Body(...),
    location: Location = Body(...),
):
    return {**dict(person), **dict(location)}

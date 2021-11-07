# Python
from typing import Dict, Optional
from enum import Enum

# Pydantic
from pydantic import BaseModel, Field
from pydantic import EmailStr

# FastAPI
from fastapi import FastAPI
from fastapi import status
from fastapi import HTTPException
from fastapi import Body, Query, Path, Form, Header, Cookie, File, UploadFile


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


class LoginOut(BaseModel):
    username: str = Field(..., max_length=20, example="stivenramireza")
    message: str = Field(default="Login successfully!")


@app.get(path="/", status_code=status.HTTP_200_OK, tags=["Home"])
def home() -> Dict[str, any]:
    return {"Hello": "World"}


# Request and Response Body
@app.post(
    path="/person/new",
    response_model=PersonOut,
    status_code=status.HTTP_201_CREATED,
    tags=["People"],
    summary="Create person in the app",
)
def create_person(person: Person = Body(...)) -> Dict[str, any]:
    """
    Create Person

    This path operation creates a person in the app and save the information in the database

    Parameters:
    - Request body parameter:
        - **person: Person** -> A person model with first name, last name, age, hair color and marital status

    Returns a person model with first name, last name, age, hair color and marital status
    """
    return person


# Validations: Query Parameters
@app.get(
    path="/person/detail",
    status_code=status.HTTP_200_OK,
    tags=["People"],
    deprecated=True,
)
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


persons = [1, 2, 3, 4, 5]

# Validations: Path Parameters
@app.get(
    path="/person/detail/{person_id}", status_code=status.HTTP_200_OK, tags=["People"]
)
def show_person(
    person_id: int = Path(
        ...,
        gt=0,
        title="Person id",
        description="This is the person id. It's required",
        example=123,
    )
) -> Dict[str, any]:
    if person_id not in persons:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="This person doesn't exist"
        )
    return {person_id: "It exists!"}


# Validations: Request Body
@app.put(
    path="/person/{person_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["People"]
)
def update_person(
    person_id: int = Path(
        ..., title="Person id", description="This is the person id", gt=0, example=123
    ),
    person: Person = Body(...),
    location: Location = Body(...),
) -> Dict[str, any]:
    return {**dict(person), **dict(location)}


# Forms
@app.post(
    path="/login",
    response_model=LoginOut,
    status_code=status.HTTP_200_OK,
    tags=["People"],
)
def login(username: str = Form(...), password: str = Form(...)) -> Dict[str, any]:
    return LoginOut(username=username)


# Cookies and Headers Parameters
@app.post(path="/contact", status_code=status.HTTP_200_OK, tags=["Contacts"])
def contact(
    first_name: str = Form(..., min_length=1, max_length=20),
    last_name: str = Form(..., min_length=1, max_length=20),
    email: EmailStr = Form(...),
    message: str = Form(..., min_length=20),
    user_agent: Optional[str] = Header(default=None),
    ads: Optional[str] = Cookie(default=None),
) -> Dict[str, any]:
    return user_agent


# Files
@app.post(path="/post-image", tags=["Files"])
def post_image(image: UploadFile = File(...)) -> Dict[str, any]:
    return {
        "Filename": image.filename,
        "Format": image.content_type,
        "Size(KB)": round(len(image.file.read()) / 1024, ndigits=2),
    }

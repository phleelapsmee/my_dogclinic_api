from enum import Enum
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, Query
from typing import List

app = FastAPI()

class DogType(str, Enum):
    terrier = "terrier"
    bulldog = "bulldog"
    dalmatian = "dalmatian"

class Dog(BaseModel):
    name: str
    pk: int
    kind: DogType

class Timestamp(BaseModel):
    id: int
    timestamp: int

dogs_db = {
    0: Dog(name='Bob', pk=0, kind='terrier'),
    1: Dog(name='Marli', pk=1, kind="bulldog"),
    2: Dog(name='Snoopy', pk=2, kind='dalmatian'),
    3: Dog(name='Rex', pk=3, kind='dalmatian'),
    4: Dog(name='Pongo', pk=4, kind='dalmatian'),
    5: Dog(name='Tillman', pk=5, kind='bulldog'),
    6: Dog(name='Uga', pk=6, kind='bulldog')
}

post_db = [
    Timestamp(id=0, timestamp=12),
    Timestamp(id=1, timestamp=10)
]

@app.get("/")
def root():
    return {"message": "Hello, student!"}

@app.post("/post", response_model=Timestamp)
def create_post():
    return post_db[0]

@app.get("/dog", response_model=List[Dog])
def read_dogs(kind: DogType = Query(None)):
    if kind:
        filtered_dogs = [dog for dog in dogs_db.values() if dog.kind == kind]
        return filtered_dogs
    return list(dogs_db.values())

@app.post("/dog", response_model=Dog)
def create_dog(dog: Dog):
    pk = max(dogs_db.keys()) + 1
    dog.pk = pk
    dogs_db[pk] = dog
    return dog

@app.get("/dog/{pk}", response_model=Dog)
def read_dog(pk: int):
    if pk in dogs_db:
        return dogs_db[pk]
    raise HTTPException(status_code=404)

@app.patch("/dog/{pk}", response_model=Dog)
def update_dog(pk: int, updated_dog: Dog):
    if pk in dogs_db:
        dogs_db[pk].name = updated_dog.name
        dogs_db[pk].kind = updated_dog.kind
        return dogs_db[pk]
    raise HTTPException(status_code=404)
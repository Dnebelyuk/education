from typing import List, Optional

from pydantic import BaseModel, Field
from datetime import date


class WordsRequest(BaseModel):
    words: List[str]


class WordsResponse(BaseModel):
    unique_words: List[str]


class ConverterRequest(BaseModel):
    number: int | str


class ConverterResponse(BaseModel):
    arabic: int
    roman: str


class User(BaseModel):
    name: str
    age: int = Field(..., ge=0, le=100, description="Возраст не может быть меньше 0 и больше 100")
    adult: bool = None
    message: Optional[str] = None


class Mapping(BaseModel):
    list_of_ids: List[int | str]
    tags: List[str | None]


class Meta(BaseModel):
    last_modification: date
    list_of_skills: List[str] = []  # необязательное
    mapping: Mapping


class BigJson(BaseModel):
    user: User
    meta: Meta


class GenerateFileRequest(BaseModel):
    file_type: str
    matrix_size: int = Field(..., ge=4, le=15, description="число от 4 до 15")


class GenerateFileResponse(BaseModel):
    file_id: int


# class UserRequest(BaseModel):
#     name: str
#     message: str
#
#
# class User(BaseModel):
#     name: str
#     age: str
#     is_adult: bool
#     message: str = None
#
#
# class UserResponse(BaseModel):
#     pass

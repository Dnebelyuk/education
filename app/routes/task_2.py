from fastapi import APIRouter

from app.core import convert_arabic_to_roman, convert_roman_to_arabic
from app.models import ConverterResponse, ConverterRequest


router = APIRouter(tags=["Стажировка"])

"""
Задание_2. Конвертер
    1. Реализовать функции convert_arabic_to_roman() и convert_roman_to_arabic() из пакета app.core
    2. Написать логику и проверки для вводимых данных. Учитывать, что если арабское число выходит за пределы 
    от 1 до 3999, то возвращать "не поддерживается"
    3. Запустить приложение и проверить результат через swagger
        Принимает арабское или римское число.
    Конвертирует его в римское или арабское соответственно.
    Возвращает первоначальное и полученное числа в виде json:
    {
        "arabic": 10,
        "roman": "X"
    }
"""


@router.post("/converter", response_model=ConverterResponse, description="Задание_2. Конвертер")
async def convert_number(res: ConverterRequest) -> ConverterResponse:
    number = res.number
    if isinstance(number, int):
        roman_num = convert_arabic_to_roman(number)
        return ConverterResponse(arabic=number, roman=roman_num)
    elif isinstance(number, str):
        arabic_num = convert_roman_to_arabic(number)
        return ConverterResponse(arabic=arabic_num, roman=number)



from fastapi import FastAPI, APIRouter
from app.core import remove_duplicates
from app.models import WordsResponse, WordsRequest

router = APIRouter(tags=["Стажировка"])


"""
Задание_1. Удаление дублей
    Реализуйте функцию соответствующую следующему описанию:
    На вход подаётся массив слов зависимых от регистра, для которых необходимо произвести
    фильтрацию на основании дублей слов, если в списке найден дубль по регистру, то все
    подобные слова вне зависимости от регистра исключаются.
    На выходе должны получить уникальный список слов в нижнем регистре.

    Список слов для примера: ['Мама', 'МАМА', 'Мама', 'папа', 'ПАПА', 'Мама', 'ДЯдя', 'брАт', 'Дядя', 'Дядя', 'Дядя']
    Ожидаемый результат: ['папа','брат']
"""


@router.post("/remove_duplicates", response_model=WordsResponse)
async def remove_duplicates_endpoint(req: WordsRequest) -> WordsResponse:
    unique_words = remove_duplicates(req.words)
    return WordsResponse(unique_words=unique_words)


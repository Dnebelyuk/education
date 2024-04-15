from fastapi import APIRouter, Response
from functools import wraps

router = APIRouter(tags=["Стажировка"])

"""
Задание_8. Декоратор - счётчик запросов.

Напишите декоратор который будет считать кол-во запросов сделанных к приложению.
Оберните роут new_request() этим декоратором.
Подумать, как хранить переменную с кол-вом сделаных запросов.
"""

""" Создаем глобальную переменную для хранения счетчика запросов """
request_counter = 0


def count_requests(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        global request_counter
        request_counter += 1
        return await func(*args, **kwargs)

    return wrapper


@router.get("/new_request", description="Задание_8. Декоратор - счётчик запросов.")
@count_requests
async def new_request():
    # Возвращаем кол-во сделанных запросов
    return Response(content=f"Количество запросов: {request_counter}")

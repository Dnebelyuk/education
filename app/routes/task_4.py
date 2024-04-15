from fastapi import APIRouter, File, UploadFile, HTTPException

from app.core import average_age_by_position


router = APIRouter(tags=["Стажировка"])


"""
Задание_4. Работа с pandas и csv. 

В модуле app.core реализуйте функцию average_age_by_position(), 
которая принимает на вход CSV файл с данными о сотрудниках компании. 

В файле должны быть следующие колонки: "Имя", "Возраст", "Должность". 
Функция должна вернуть словарь, в котором ключами являются уникальные должности, 
а значениями — средний возраст сотрудников на каждой должности. 
Для чтения и работы с csv файлами, нужно использовать библиотеку pandas.

Пример CSV файла (employees.csv): 
Имя,Возраст,Должность
Алексей,25,Разработчик
Мария,30,Менеджер
Иван,28,Разработчик
Анна,35,Менеджер


Роут так же должен принимать на входе csv файл.
Пример ответа:
{
    "Разработчик": 26.5,
    "Менеджер": 32.5
}

Рекомендуется добавить аннотации типов. Также добавьте исключения, если файл приходит не валидный, например, 
неправильный формат файла, названия столбцов отличаются и т.д. 
В таких случаях ожидается строка с ошибкой и status code 400.
"""


@router.post("/get_average_age_by_position", description="Задание_4. Работа с pandas и csv")
async def get_average_age_by_position(file: UploadFile = File(...)):
    try:
        # Сохраняем загруженный файл
        with open("file.csv", "wb") as buffer:
            buffer.write(await file.read())
        # Вычисляем средний возраст по должностям
        result = average_age_by_position("file.csv")
        return result

    except HTTPException as e:
        raise e

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))




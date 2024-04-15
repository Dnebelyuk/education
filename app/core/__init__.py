from abc import ABC, abstractmethod
from io import StringIO
import json
import csv
import yaml
import random

from fastapi import FastAPI, UploadFile, File, HTTPException
import pandas as pd
from typing import Dict, List


def remove_duplicates(words: List[str]) -> List[str]:
    word_count = {}
    unique_words = list(set([word.lower() for word in words]))
    for word in words:
        if word in word_count:
            word_count[word] += 1
        else:
            word_count[word] = 1

    for word in words:
        if (word_count[word] >= 2) and (word.lower() in unique_words):
            unique_words.remove(word.lower())

    return unique_words


def convert_arabic_to_roman(number: int) -> str:
    if 1 <= number <= 3999:
        val = [
            1000, 900, 500, 400,
            100, 90, 50, 40,
            10, 9, 5, 4,
            1
        ]
        syms = [
            "M", "CM", "D", "CD",
            "C", "XC", "L", "XL",
            "X", "IX", "V", "IV",
            "I"
        ]
        roman_num = ''
        i = 0
        while number > 0:
            for _ in range(number // val[i]):
                roman_num += syms[i]
                number -= val[i]
            i += 1
        return roman_num
    else:
        return "не поддерживается"


def convert_roman_to_arabic(number: str) -> int:
    values = {
        'I': 1, 'V': 5, 'X': 10, 'L': 50,
        'C': 100, 'D': 500, 'M': 1000
    }
    total = 0
    prev_value = 0
    for char in number:
        if values[char] > prev_value:
            total += values[char] - 2 * prev_value
        else:
            total += values[char]
        prev_value = values[char]
    return total


# Задание 4.
def average_age_by_position(file: str) -> Dict[str, float]:
    try:
        data = pd.read_csv(file)
    except Exception:
        raise HTTPException(status_code=400, detail=f"Error reading CSV file: {str(Exception)}")

    expected_columns = {"Имя", "Возраст", "Должность"}
    if not expected_columns.issubset(data.columns):
        raise HTTPException(status_code=400,
                            detail="Invalid CSV file format. Columns must include: 'Имя', 'Возраст', 'Должность'")

    # Вычисление среднего возраста по должностям
    result = data.groupby('Должность')['Возраст'].mean().to_dict()
    return result


# Задание 6.
class BaseWriter(ABC):
    # Абстрактный класс с методом write для генерации файла

    @abstractmethod
    def write(self, data: list[list[int, str, float]]) -> StringIO:
        """
        Записывает данные в строковый объект файла StringIO
        :param data: полученные данные
        :return: Объект StringIO с данными из data
        """
        pass


class JSONWriter(BaseWriter):
    """Потомок BaseWriter с переопределением метода write для генерации файла в json формате"""

    def write(self, data: list[list[int, str, float]]) -> StringIO:
        output = StringIO()
        json.dump(data, output)
        output.seek(0)
        return output


class CSVWriter:
    """Потомок BaseWriter с переопределением метода write для генерации файла в csv формате"""

    def write(self, data: list[list[int, str, float]]) -> StringIO:
        output = StringIO()
        writer = csv.writer(output)
        writer.writerows(data)
        output.seek(0)
        return output


class YAMLWriter:
    """Потомок BaseWriter с переопределением метода write для генерации файла в yaml формате"""

    def write(self, data: list[list[int, str, float]]) -> StringIO:
        output = StringIO()
        yaml.dump(data, output)
        output.seek(0)
        return output


class DataGenerator:
    def __init__(self, data: list[list[int, str, float]] = None):
        self.data: list[list[int, str, float]] = data
        self.file_id = None

    def generate(self, matrix_size: int) -> None:
        """Генерирует матрицу данных заданного размера."""

       #  data: list[list[int, str, float]] = []
        data = [[random.randint(0, 100), str(i), random.uniform(0.0, 100.0)] for i in range(matrix_size)]
        self.data = data

    def to_file(self, path: str, writer: BaseWriter) -> None:
        """
        Метод для записи в файл данных полученных после генерации.
        Если данных нет, то вызывается кастомный Exception.
        :param path: Путь куда требуется сохранить файл
        :param writer: Одна из реализаций классов потомков от BaseWriter
        """

        if self.data is None:
            raise ValueError("No data to write to file.")

        with open(path, "w") as f:
            output = writer.write(self.data)
            f.write(output.getvalue())
        self.file_id = id(self.data)



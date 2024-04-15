from fastapi import APIRouter

from app.core import DataGenerator, JSONWriter, CSVWriter, YAMLWriter
from app.models import GenerateFileRequest, GenerateFileResponse


router = APIRouter(tags=["API для хранения файлов"])

"""
Задание_6. 

Изучите следущие классы в модуле app.core: BaseWriter, DataGenerator

API должно принимать json, по типу:
{
    "file_type": "json",  # или "csv", "yaml"
    "matrix_size": int    # число от 4 до 15
}
В ответ на удачную генерацию файла должен приходить id для скачивания.

Добавьте реализацию методов класса DataGenerator.
Добавьте аннотации типов и (если требуется) модели в модуль app.models.

(Подумать, как переисползовать код из задания 5)
"""


@router.post("/generate_file", response_model=GenerateFileResponse, description="Задание_6. Конвертер")
async def generate_file(request_body: GenerateFileRequest):

    data = DataGenerator()
    data.generate(request_body.matrix_size)

    if request_body.file_type == "json":
        writer = JSONWriter()
    elif request_body.file_type == "csv":
        writer = CSVWriter()
    elif request_body.file_type == "yaml":
        writer = YAMLWriter()
    else:
        return "Unsupported file type. Only 'json', 'csv', or 'yaml' are supported."

    data.to_file("generated_file." + request_body.file_type, writer)

    return GenerateFileResponse(file_id=data.file_id)

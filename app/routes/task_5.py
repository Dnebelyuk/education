import zipfile

from fastapi import APIRouter, File, UploadFile, HTTPException, Response
from zipfile import ZipFile
from fastapi.responses import FileResponse
import os
import shutil

router = APIRouter(tags=["API для хранения файлов"])

"""
Задание_5. API для хранения файлов

a.	Написать API для добавления(POST) "/upload_file" и скачивания (GET) "/download_file/{id}" файлов. 
В ответ на удачную загрузку файла должен приходить id для скачивания. 
b.	Добавить архивирование к post запросу, то есть файл должен сжиматься и сохраняться в ZIP формате.
с*.Добавить аннотации типов.
"""


@router.post("/upload_file/", description="Задание_5. API для хранения файлов")
async def upload_file(file: UploadFile = File(...)) -> str:
    try:
        # Сохраняем загруженный файл
        file_path = f"{file.filename}"
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Архивируем файл в ZIP
        zip_file_path = f"{file.filename}.zip"
        with ZipFile(zip_file_path, "w") as zipf:
            zipf.write(file_path, os.path.basename(file_path))

        return os.path.basename(zip_file_path)

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error uploading file: {str(e)}")
#   file_id: int
 #   return file_id


@router.get("/download_file/{id}", description="Задание_5. API для хранения файлов")
async def download_file(id: str):
    try:
        # Отправляем пользователю архивированный файл
        file_path = f"{id}"

        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="File not found")

        return FileResponse(file_path, media_type='application/zip', filename=id)

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error downloading file: {str(e)}")

 #   file = None

  #  return file


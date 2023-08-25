import os
import shutil
import uuid

from fastapi import UploadFile
from sqlalchemy.orm import Session


async def upload_file(
        file: UploadFile,
        db: Session
):
    destination_path = "src/uploads"
    file_folder_path = os.path.join(destination_path, str(uuid.uuid4()))
    os.makedirs(file_folder_path, exist_ok=True)
    file_path = os.path.join(file_folder_path, file.filename)

    # safe copy and save file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "file_path": file_path
    }

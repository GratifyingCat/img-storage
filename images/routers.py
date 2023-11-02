import os
import uuid
from PIL import Image

from fastapi import APIRouter, Depends, UploadFile, status
from fastapi.exceptions import HTTPException

from sqlalchemy.orm import Session

from . import crud
from . import schemas
from database.database import get_db


router = APIRouter(
    prefix='/images',
    tags=['images']
)


@router.post('/upload')
def upload_image(image_file: UploadFile, 
                 db: Session = Depends(get_db)):
    path = os.path.join('media', 'images')
    if not os.path.exists(path):
        os.makedirs(path)
    image_format = image_file.content_type.split('/')[1]
    image_unique_name = str(uuid.uuid1()) + '.' + image_format
    image_path = os.path.join(path, image_unique_name)
    img = Image.open(image_file.file)
    img.save(image_path, format=image_format)
    return crud.create_image(db, schemas.PostImage(path=image_path))


@router.get('/')
def get_images(image_id: int | None = None, 
               db: Session = Depends(get_db)):
    if image_id:
        db_image = crud.get_image(db, image_id)
        if not db_image:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return db_image
    db_images = crud.get_images(db)
    if not db_images:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return db_images


@router.delete('/delete')
def delete_images(image_id: int | None = None,
                  db: Session = Depends(get_db)):
    if image_id:
        deleted_image = crud.delete_images(db, image_id)
        if not deleted_image:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        os.remove(deleted_image.path)
        return deleted_image
    deleted_images = crud.delete_images(db)
    if not deleted_images:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    for d_img in deleted_images:
        os.remove(d_img.path)
    return deleted_images
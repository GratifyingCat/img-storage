from sqlalchemy.orm import Session

from . import schemas
from . import models


def create_image(db: Session, image: schemas.PostImage) -> models.Image:
    db_image = models.Image(path=image.path)
    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    return db_image


def get_images(db: Session) -> list[models.Image]:
    return db.query(models.Image).all()


def get_image(db: Session, image_id: int) -> models.Image:
    return db.query(models.Image).filter_by(id=image_id).one()


def delete_images(db: Session, image_id: int | None = None) -> models.Image | list[models.Image]:
    if image_id:
        db_image = get_image(db, image_id)
        db.delete(db_image)
        db.commit()
        return db_image
    db_images = get_images(db)
    for img in db_images:
        db.delete(img)
    db.commit()
    return db_images
from fastapi import APIRouter


router = APIRouter(
    prefix='/accounts',
    tags=['accounts']
)


@router.get('/token')
def token():
    return {'token': 'token'}
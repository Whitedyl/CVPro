from fastapi import APIRouter

router = APIRouter(prefix="/job", tags=["Job"])


@router.get("/job")
def test():
    return{"message": "job endpoint working"}

from fastapi import APIRouter

router = APIRouter()


@router.get("/api/users/", tags=["users"])
async def read_users():
    return [{"username": "Ash"}, {"username": "Ben"}]

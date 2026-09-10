from fastapi import APIRouter

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.get("/demo")
def demo_auth_check():
    return {"message": "auth router ready"}

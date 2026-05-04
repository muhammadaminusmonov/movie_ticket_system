from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app.core.deps import get_db, get_current_user, require_admin, require_owner
from app.services.cinema_service import CinemaService

router = APIRouter()


class CinemaCreateRequest(BaseModel):
    name: str
    location: str
    owner_id: str


class CinemaUpdateRequest(BaseModel):
    name: str | None = None
    location: str | None = None


@router.get("/", summary="List all cinemas (public)")
def get_cinemas(db=Depends(get_db)):
    return CinemaService(db).get_all_cinemas()


@router.get("/mine", summary="Get my cinemas (Owner)")
def get_my_cinemas(current_user: dict = Depends(get_current_user), db=Depends(get_db)):
    return CinemaService(db).get_my_cinemas(current_user["user_id"])


@router.get("/{cinema_id}", summary="Get cinema details (public)")
def get_cinema(cinema_id: str, db=Depends(get_db)):
    try:
        return CinemaService(db).get_cinema(cinema_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/", summary="Create a cinema (Admin)")
def create_cinema(body: CinemaCreateRequest, db=Depends(get_db), _=Depends(require_admin)):
    try:
        return CinemaService(db).create_cinema(
            name=body.name,
            location=body.location,
            owner_id=body.owner_id,
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{cinema_id}", summary="Update a cinema (Admin)")
def update_cinema(cinema_id: str, body: CinemaUpdateRequest, db=Depends(get_db), _=Depends(require_admin)):
    try:
        return CinemaService(db).update_cinema(cinema_id, name=body.name, location=body.location)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{cinema_id}", summary="Delete a cinema (Admin)")
def delete_cinema(cinema_id: str, db=Depends(get_db), _=Depends(require_admin)):
    try:
        CinemaService(db).delete_cinema(cinema_id)
        return {"success": True}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


# ── Admin: Manage Cinema Owners ──────────────────────────────────────────────

@router.get("/owners/list", summary="List all cinema owners (Admin)")
def list_owners(db=Depends(get_db), _=Depends(require_admin)):
    return CinemaService(db).list_owners()


@router.post("/owners/{user_id}/promote", summary="Promote user to Cinema Owner (Admin)")
def promote_to_owner(user_id: str, db=Depends(get_db), _=Depends(require_admin)):
    try:
        return CinemaService(db).assign_owner_role(user_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
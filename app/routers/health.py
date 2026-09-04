from fastapi import APIRouter

router = APIRouter(tags=["Health"])


@router.get("/health")
def health() -> dict[str, str]:
    """Liveness check used by local runs and Docker."""
    return {"status": "ok"}

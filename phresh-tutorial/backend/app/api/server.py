from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes import router as api_router


def get_application() -> FastAPI:
    app = FastAPI(title="API-tutorial", version="0.0.1")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
        allow_credentials=True,
    )

    app.include_router(api_router, prefix="/api")

    return app


app = get_application()

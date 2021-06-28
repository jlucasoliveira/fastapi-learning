from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from ..core import config, tasks
from .routes import router as api_router


def get_application() -> FastAPI:
    app = FastAPI(title=config.PROJECT_NAME, version=config.VERSION)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
        allow_credentials=True,
    )

    app.add_event_handler("startup", tasks.create_start_app_handler(app))
    app.add_event_handler("shutdown", tasks.create_stop_app_handler(app))

    app.include_router(api_router, prefix=config.API_PREFIX)

    return app


app = get_application()
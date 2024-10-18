from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.utils import constant

SECRET_KEY = constant.secrets_key


def get_app() -> FastAPI:
    app = FastAPI()

    origins = ["*"]
    # app.router.prefix = "/api/v1"

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,  # Restrict this to specific domains if needed
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return app

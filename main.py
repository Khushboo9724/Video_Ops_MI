import uvicorn

from app import get_app

from app.routes.api_routes import router as api_router

app = get_app()

app.include_router(api_router)

if __name__ == '__main__':
    uvicorn.run("main:app", host='0.0.0.0', port=8002, log_level="info", reload=True)

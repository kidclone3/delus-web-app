import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
#
from src.config.app_configs import app_configs, settings
from src.controllers.home_controller import router as home_router

app = FastAPI(**app_configs)
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=settings.CORS_ORIGINS,
#     allow_credentials=True,
#     allow_methods=("GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"),
#     allow_headers=settings.CORS_HEADERS,
# )


@app.get("/healthcheck")
async def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


# app.include_router(home_router, prefix="/home", tags=["Home"])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

#
from src.config.app_configs import app_configs, settings
from src.controllers.home_controller import router as home_router
from src.controllers.chatbot_controller import router as chatbot_router
from src.controllers.olp_controller import router as olp_router
from src.controllers.driver_controller import router as driver_router
from src.controllers.ride_controller import router as ride_router
from src.controllers.customer_controller import router as customer_router

app = FastAPI(**app_configs)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=("GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"),
    allow_headers=settings.CORS_HEADERS,
)


@app.get("/healthcheck")
async def healthcheck() -> dict[str, str]:
    return {"status": "ok"}

@app.get("/")
def main():
    return {"message": "Hello World"}

app.include_router(home_router, prefix="/home", tags=["Home"])
app.include_router(chatbot_router, prefix="/chatbot", tags=["Chatbot"])
app.include_router(olp_router, prefix="/olp", tags=["OLP"])
app.include_router(driver_router, prefix="/drivers", tags=["Driver"])
app.include_router(ride_router, prefix="/rides", tags=["Ride"])
app.include_router(customer_router, prefix="/customers", tags=["Customer"])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8005)

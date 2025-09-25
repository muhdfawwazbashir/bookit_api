from fastapi import FastAPI
from app.api import auth, users


app = FastAPI()


@app.get("/")
async def read_root():
    return {"message: Welcome to BookIt API"}


app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(users.router, prefix="/me", tags=["Users"])
# app.include_router(services.router, prefix="/services", tags=["services"])
# app.include_router(bookings.router, prefix="/bookings", tags=["bookings"])
# app.include_router(reviews.router, prefix="/reviews", tags=["reviews"])
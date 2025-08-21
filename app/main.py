from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from contextlib import asynccontextmanager
from app.api import router as api_router
from app.database import create_db_and_tables
from app.services.auth_service import create_access_token
from datetime import timedelta

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Code to run on startup
    create_db_and_tables()
    print("Database tables created.")
    yield
    # Code to run on shutdown (e.g., close connections)
    print("Application shutting down.")

app = FastAPI(lifespan=lifespan)

app.include_router(api_router)

@app.post("/token", response_model=dict)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    # In a real app, you would verify the user's password from a database.
    # For this example, we'll accept any username with a dummy password "test".
    if form_data.password != "test":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": form_data.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
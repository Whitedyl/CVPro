from fastapi import FastAPI, Depends, HTTPException
from app.routes import cv, jobdes
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.database import Base, engine, get_db
from app.models import Candidate



Base.metadata.create_all(bind=engine)

app = FastAPI(title="CV Matcher App")

app.include_router(cv.router)
app.include_router(jobdes.router)

@app.get("/db-test")
def db_test(db: Session = Depends(get_db)):
    try:
        # Run a simple query to check connection
        db.execute(text("SELECT 1"))
        return {"status": "Database connected successfully!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection failed: {e}")
@app.get("/")
def home():
    return{"message": "CV Matcher is running"}
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Candidate
import PyPDF2
import docx
from app.utils.cv_parser import extract_text_from_pdf, extract_text_from_docx


router = APIRouter()



@router.post("/upload-cv")
async def upload_cv(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    
    #validating file type
    filename = file.filename.lower()
    if not(filename.endswith(".pdf") or filename.endswith(".docx")):
        raise HTTPException(status_code=400, detail="Unsupported file type. Please upload a PDF or docx file!")
    
    #Reading the file content(in bytes)
    content = await file.read()

    #Extrating text
    if filename.endswith(".pdf"):
        extracted_text = extract_text_from_pdf(content)
    else:
        extracted_text = extract_text_from_docx(content)
        
    #check extraction was successful
    if not extracted_text.strip():
        raise HTTPException(status_code=400, detail="Could not extract text from file")
    

    #Creating candidate instance to save to db
    candidate = Candidate(
        name = "",
        email = None,
        skills =[],
        experience = 0,
        cv_text = extracted_text,
        feedback = None
    )

    #Save to db
    try:
        db.add(candidate)
        db.commit()
        db.refresh(candidate)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to save CV: {e}")
    
    return {"message": "CV was uploaded successfully!", "candidate_id ": candidate.id}


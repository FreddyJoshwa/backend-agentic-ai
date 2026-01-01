from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.resume import Resume
from app.core.security import HTTPBearer, verify_token
import os
from app.utils.parcer import parse_resume, analyze_resume

router = APIRouter()
security = HTTPBearer()
UPLOAD_DIR = "uploaded_resumes"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/resume")
async def upload_resume(
    resume_file: UploadFile = File(...),
    goals: str = Form(...),
    credentials = Depends(security),
    db: Session = Depends(get_db)
):
    payload = verify_token(credentials.credentials)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    user_id = int(payload.get("sub"))

    # Save file
    file_path = os.path.join(UPLOAD_DIR, f"{user_id}_{resume_file.filename}")
    with open(file_path, "wb") as f:
        content = await resume_file.read()
        f.write(content)

    # Parse & Analyze resume
    text = parse_resume(file_path)
    analysis = analyze_resume(text, goals)

    # Save to DB
    resume = db.query(Resume).filter(Resume.user_id == user_id).first()
    if resume:
        resume.resume_file = file_path
        resume.goals = goals
        resume.skills = ",".join(analysis["skills"])
        resume.missing_skills = ",".join(analysis["missing_skills"])
    else:
        resume = Resume(
            user_id=user_id,
            resume_file=file_path,
            goals=goals,
            skills=",".join(analysis["skills"]),
            missing_skills=",".join(analysis["missing_skills"])
        )
        db.add(resume)

    db.commit()
    db.refresh(resume)

    return {
        "message": "Resume uploaded and analyzed",
        "skills": analysis["skills"],
        "missing_skills": analysis["missing_skills"],
        "goals": goals
    }

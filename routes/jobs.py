from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from database import get_db
import models, schemas
from auth import get_current_user
from fastapi import HTTPException
from sqlalchemy import or_

router= APIRouter(prefix="/jobs",tags=["jobs"])

@router.post("/",response_model=schemas.JobResponse)
def create_job(
    job: schemas.JobCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    new_job = models.Job(
        title=job.title,
        company=job.company,
        status=job.status,
        salary=job.salary,
        user_id=current_user.id
    )

    db.add(new_job)
    db.commit()
    db.refresh(new_job)

    return new_job

@router.get("/",response_model=list[schemas.JobResponse])
def get_jobs(
    search:str|None=None,
    status: str|None=None,
    sort:str|None=None,
    skip:int=0,
    limit:int=10,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    query = db.query(models.Job).filter(
        models.Job.user_id == current_user.id
    )

    if search:
        query=query.filter(or_(models.Job.title.contains(search),
                           models.Job.company.contains(search)))


    if status:
        query=query.filter(models.Job.status==status)
    
    if sort =="latest":
        query=query.order_by(models.Job.id.desc())
    elif sort=="oldest":
        query=query.order_by(models.Job.id.asc())

    jobs=query.offset(skip).limit(limit).all()

    return jobs

@router.put("/{job_id}",response_model=schemas.JobResponse)
def update_job(
    job_id:int,
    job:schemas.JobCreate,
    db:Session=Depends(get_db),
    current_user=Depends(get_current_user)

):
    existing_job=db.query(models.Job).filter(models.Job.id==job_id,
                                             models.Job.user_id==current_user.id).first()
    
    if not existing_job:
        raise HTTPException(status_code=404,detail="job not found")
    
    existing_job.title=job.title
    existing_job.company=job.company
    existing_job.status=job.status
    existing_job.salary=job.salary

    db.commit()
    db.refresh(existing_job)

    return existing_job

@router.put("/{job_id}/status",response_model=schemas.JobResponse)
def update_status(
    job_id: int,
    status: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    job = db.query(models.Job).filter(
        models.Job.id == job_id,
        models.Job.user_id == current_user.id
    ).first()

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    job.status = status

    db.commit()
    db.refresh(job)

    return job
    
@router.delete("/{job_id}",response_model=schemas.JobResponse)
def delete_job(job_id:int,db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    job = db.query(models.Job).filter(models.Job.id==job_id,models.Job.user_id==current_user.id).first()

    if not job:
       raise HTTPException(status_code=404,detail="job not found")
                
    db.delete(job)
    db.commit()



@router.get("/all")
def get_all_jobs(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not allowed")

    jobs = db.query(models.Job).all()
    return jobs


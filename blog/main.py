from fastapi import FastAPI, Depends, status, Response, HTTPException
from . import schemas
from . import models
from .database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()

# making table 
models.Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# creating a blog   
@app.post('/blog',status_code=status.HTTP_201_CREATED)
def create(request:schemas.Blog , db:Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title,body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.delete('/blog/{id}',status_code=status.HTTP_204_NO_CONTENT)
def destroy(id, db: Session = Depends(get_db)):
    db.query(models.Blog).filter(models.Blog.id==id).delete(synchronize_session=False)
    db.commit()
    return f'deleted blog {id}'

@app.get('/blog')
def get_all(db:Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

@app.put('/blog/{id}',status_code=status.HTTP_202_ACCEPTED)
def update(id,request:schemas.Blog, db:Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).update(request.dict())
    if not blog.first():
        raise HTTPException(statu_code=status.HTTP_404_NOT_FOUND,details='blog not found')
    db.commit()
    return 'updated successfully'



@app.get('/blog/{id}')
def show(id,response:Response, db:Session = Depends(get_db), status_code=200):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,details='there is no blog for this id')
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return "there is no blog for this id"
    return blog
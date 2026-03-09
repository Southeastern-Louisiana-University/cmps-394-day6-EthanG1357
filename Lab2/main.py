from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import engine, SessionLocal
import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/{username}")
def create_user(username: str, db: Session = Depends(get_db)):
    user = models.User(username=username)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@app.get("/users")
def get_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()


@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
    return {"message": "Deleted if existed"}

@app.post("/posts/{user_id}")
def create_post(user_id: int, db: Session = Depends(get_db)):
    post = models.Post(
        title="Sample Title",
        content="Sample Content",
        user_id=user_id
    )
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    return db.query(models.Post).all()


@app.delete("/posts/{post_id}")
def delete_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if post:
        db.delete(post)
        db.commit()
    return {"message": "Deleted if existed"}




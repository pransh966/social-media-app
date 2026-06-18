from operator import index
import fastapi
from fastapi import FastAPI, Query,Response, status, HTTPException,Depends
from fastapi.params import Body
from httpx import post
from typing import Optional, List
from random import randrange

from app import oauth2
from . import model,schemas
from .database import engine, SessionLocal, Base,get_db
from sqlalchemy.orm import Session
import app.utils as utils
from app.routers import post, user, auth
from .config import settings


model.Base.metadata.create_all(bind=engine)
app = FastAPI()
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/posts", response_model=list[schemas.postresponse])
def read_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int =Query(10, ge=1, le=100),
skip: int=Query(0, ge=0), search: Optional[str]=""):
   #cursor.execute("""SELECT * FROM posts""")
    #posts=cursor.fetchall()
    post=db.query(model.Post).filter(model.Post.title.contains(search)).limit(limit).offset(skip).all()
    return post

@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.postresponse)
def create_post(post: schemas.postcreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    #cursor.execute("""INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING *""", (post.title, post.content, post.published))
    #new_post = cursor.fetchone()
    #conn.commit()
    new_post = model.Post(Owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@app.get("/posts/latest", response_model=schemas.postresponse)
def get_latest_post():
    post=post[len(post)-1]
    return post

@app.get("/posts/{id}", response_model=schemas.postresponse)
def get_post(id: int, db: Session = Depends(get_db)):
    #cursor.execute("""SELECT * FROM posts WHERE ID=%s""",(str(id)))
    #post=cursor.fetchone()
    post = db.query(model.Post).filter(model.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")  
    print(post)
    return post 

@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    #delete post
    #find the index in the array that has required id
    #my_post.pop(index)
    #cursor.execute("""DELETE FROM posts WHERE ID=%s RETURNING *""",(str(id)))
    #deleted_post=cursor.fetchone()
   # conn.commit()
    post = db.query(model.Post).filter(model.Post.id == id)
    post_delete = post.first()
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} does not exist"
        )

    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}", response_model=schemas.postresponse)
def update_post(id: int, updated_post: schemas.postcreate, db: Session = Depends(get_db)):
   
   #cursor.execute("""UPDATE posts SET title=%s, content=%s, published=%s WHERE ID=%s RETURNING *""",(post.title, post.content, post.published, str(id)))
   #updated_post=cursor.fetchone()
   #conn.commit()
    post_query = db.query(model.Post).filter(model.Post.id == id)
    post = post_query.first()

    
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} does not exist"
        )

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return  post_query.first() 

#-------------------------------------------------------------------------------

@app.post("/users",status_code=status.HTTP_201_CREATED, response_model=schemas.userresponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    #hash the password - user.password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user=model.User(email=user.email, password=user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
@app.get("/users/{id}", response_model=schemas.userresponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(model.User).filter(model.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id: {id} was not found")  
    print(user)
    return user


from fastapi import APIRouter, Query
from app import model, oauth2, schemas, utils
from .. import model,schemas,utils
from fastapi import FastAPI, Response, status, HTTPException, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List, Optional

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)


@router.get("/", response_model=list[schemas.postresponse])
def read_posts(db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user), limit: int =Query(10 ,ge=1 ,le=100),
skip: int=Query(0, ge=0),search: Optional[str]=""):
   #cursor.execute("""SELECT * FROM posts""")
    #posts=cursor.fetchall()s
     posts = db.query(model.Post).filter(model.Post.title.contains(search)).limit(limit).offset(skip).all()
     return posts

     
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.postresponse)
def create_post(post: schemas.postcreate, db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    #cursor.execute("""INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING *""", (post.title, post.content, post.published))
    #new_post = cursor.fetchone()
    #conn.commit()
    print(current_user.id)
    new_post = model.Post(Owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/latest", response_model=schemas.postresponse)
def get_latest_post():
    post=post[len(post)-1]
    return post

@router.get("/{id}", response_model=schemas.postresponse)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    #cursor.execute("""SELECT * FROM posts WHERE ID=%s""",(str(id)))
    #post=cursor.fetchone()
    post = db.query(model.Post).filter(model.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")  
    print(post)
    return post 

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
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
    if post_delete.Owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.postresponse)
def update_post(id: int, updated_post: schemas.postcreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
   
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
    if post.Owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return  post_query.first() 
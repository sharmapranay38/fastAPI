from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
import uvicorn
app = FastAPI()

class Blog(BaseModel):
    title: str
    body: str
    published: Optional[bool]

@app.get('/blog')
def index(limit=10,published:bool = True,sort: Optional['str'] = None):
    s = f'{10} blogs are being displayed'
    if published:
        s = s+' and they are published'
    else:
        s = s+' but they are not published'
    return s

@app.get('/about')
def about():
    return "this is about page"

@app.get('/blog/unpublished')
def unpublished():
    return {'data':'unpublished'}


@app.get('/blog/{id}')
def show(id:int ):
    return {'data':id}


@app.get('/blog/{id}/comments')
def comments(id,limit=10):
    return f"showing the first {limit} comments"


@app.post('/blog')
def create_blog(request:Blog):
    return {'data':f'this is the body : {request.body}'}
    return {'data':'blog is created'}   

if __name__ == "__main__":
    uvicorn.run(app,host='127.0.0.1',port=6969)
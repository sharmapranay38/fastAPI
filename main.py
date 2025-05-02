from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def index():
    return {'data':{'name':'pranay','age':20}}

@app.get('/about')
def about():
    return "this is about page"
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import uvicorn

app = FastAPI()
templates = Jinja2Templates(directory='D:\SoftPython\python\pruebas')

@app.post('/submit')
def submit(car: str = Form(...)):
    return car

@app.get('/', response_class=HTMLResponse)
def main(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})


if __name__=='__main__':
   
    uvicorn.run(app, host="localhost", port=8080)
from fastapi import APIRouter #Importar modulo
import uvicorn #importar
from fastapi import Request, FastAPI, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from funcion_insertar import *
import asyncio



templates = Jinja2Templates(directory="D:/static/")
appr = APIRouter()

#appr.mount("/static", StaticFiles(directory="D:/static/html"), name="static")


@appr.get("/")
async def home(request: Request):
    return templates.TemplateResponse("/index.html",{"request":request})



@appr.post("/login")
def form_post(request: Request, eml: str = Form(...), psw: str = Form(...)):
    print(eml)
    print(psw)
    s=select_login(eml)
    print(s)
    return templates.TemplateResponse("/index.html",{"request":request})
    #return "LOGIN...""LOGIN..."
    #return SimpleLogin(eml=eml,psw=psw)
@appr.post('/submit')
async def submit(request: Request, car: str = Form(...), ca: str = Form(...),  fn: str = Form(...)):
    print (ca)
    print (fn)
    return car
  

    
    
    #insert_varibles_into_signup(fn, eml, psw, rpsw)
    #return templates.TemplateResponse("/index.html",{"request":request})
    #return "LOGIN...""LOGIN..."
    #return SimpleLogin(eml=eml,psw=psw)


async def main():

    config = uvicorn.Config("app1:appr", host="localhost", port=5000, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()
   
    #uvicorn.run(appr, host="localhost", port=8000)


if __name__ == "__main__":
    asyncio.run(main())

from fastapi import APIRouter #Importar modulo
import uvicorn #importar
from fastapi import Request, FastAPI, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from funcion_insertar import *



templates = Jinja2Templates(directory="C:/files/static")
appr = APIRouter()

appr.mount("/static", StaticFiles(directory="C:/files/static"), name="static")


@appr.get("/")
async def home(request: Request):
    return templates.TemplateResponse("/index.html",{"request":request})



@appr.post("/login")
def form_post(request: Request, eml: str = Form(...),psw: str = Form(...)):
    print(eml)
    print(psw)
    s=select_login(eml)
    print(s)
    return templates.TemplateResponse("/index.html",{"request":request})
    #return "LOGIN...""LOGIN..."
    #return SimpleLogin(eml=eml,psw=psw)

@appr.post("/signup")
def form_post(request: Request, fn: str = Form(...), eml: str = Form(...), psw: str = Form(...), rpsw: str = Form(...)):
    print(fn)
    print(eml)
    print(psw)
    print(rpsw)

    
    
    insert_varibles_into_signup(fn, eml, psw, rpsw)
    return templates.TemplateResponse("/index.html",{"request":request})
    #return "LOGIN...""LOGIN..."
    #return SimpleLogin(eml=eml,psw=psw)



if __name__=='__main__':
   
    uvicorn.run(appr, host="172.31.51.221", port=80)

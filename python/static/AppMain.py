from fastapi import APIRouter #Importar modulo
import uvicorn #importar
from fastapi import Request, FastAPI, Form
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from funcion_insertar import *
from funcion_select import *
import cv2

import numpy as np
from pyzbar import pyzbar


appr = FastAPI()
templates = Jinja2Templates(directory='D:\SoftPython\python\static')

appr.mount("/static", StaticFiles(directory="D:/SoftPython/python/static"), name="static")



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

@appr.get("/obtenerusr")
def homeusr(request: Request, eml: str):
    print (eml)
    print("obtener")

    
    s=select_login(eml)
    datos = {
        'titulo': 'Mi página',
        'mensaje': '¡Hola desde un endpoint!',
        'Correo': s[0][0],
        'Password': s[0][1]
            }
    
    return templates.TemplateResponse("/html/usuarios.html", {"request": request, "datos": datos})
    #return templates.TemplateResponse("item.html", {"request": request, "id": id}
def read_barcodes(frame):
    barcodes = pyzbar.decode(frame)
    for barcode in barcodes:
        x, y , w, h = barcode.rect
        #1
        barcode_info = barcode.data.decode('utf-8')
        cv2.rectangle(frame, (x, y),(x+w, y+h), (0, 255, 0), 2)
        #2
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, barcode_info, (x + 6, y - 6), font, 2.0, (255, 255, 255), 1)
        #3
        with open("barcode_result.txt", mode ='w') as file:
           file.write("Recognized Barcode:" + barcode_info)
    return frame


def generate_frames():
    #https://10.140.168.29:8008/video
    #cap = cv2.VideoCapture('http://192.168.18.37:8090/video')
    #camera = cv2.VideoCapture(0)
    camera = cv2.VideoCapture('http://10.184.204.212:8008/video')
    while True:
        ret, frame = camera.read()
        if not ret:
            break
        frame = read_barcodes(frame)
        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
    camera.release()

@appr.get("/video_feed")
async def video_feed():
    return StreamingResponse(generate_frames(), media_type="multipart/x-mixed-replace; boundary=frame")

@appr.get("/obtenervideo")
async def obtener_video(request: Request):
    return templates.TemplateResponse("/html/obtener_video.html", {"request": request})


    
if __name__=='__main__':
   
    uvicorn.run(appr, host="192.168.95.11", port=8080)

 

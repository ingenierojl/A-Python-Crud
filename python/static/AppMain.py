from fastapi import APIRouter #Importar modulo
import uvicorn #importar
from fastapi import Request, FastAPI, Form
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from funcion_insertar import *
from funcion_select import *
import cv2
import face_recognition
import numpy as np
from pyzbar import pyzbar

from fastapi import FastAPI, File, UploadFile, Form, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
import base64

from io import BytesIO
from PIL import Image
import io
import os
import PIL.Image



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





# Cargar imágenes y encodings de caras de referencia
reference_image = face_recognition.load_image_file("D:/SoftPython/python/static/photo.jpg")
reference_face_encoding = face_recognition.face_encodings(reference_image)[0]

def generate_facial_frames():
    camera = cv2.VideoCapture('http://10.184.204.212:8008/video')
    
    while True:
        ret, frame = camera.read()
        
        if not ret:
            break
        
        # Detectar caras en el fotograma actual
        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)
        
        for face_encoding in face_encodings:
            # Comparar la cara detectada con la cara de referencia
            matches = face_recognition.compare_faces([reference_face_encoding], face_encoding)
            name = "Desconocido"
            
            if matches[0]:
                name = "Persona conocida"
            
            # Dibujar un rectángulo y el nombre en el fotograma
            top, right, bottom, left = face_locations[0]
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)
        
        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
    
    camera.release()

@appr.get("/video_feed_facial")
async def video_feed_facial():
    return StreamingResponse(generate_facial_frames(), media_type="multipart/x-mixed-replace; boundary=frame")

@appr.get("/reconocimiento_facial_page")
async def reconocimiento_facial_page(request: Request):
    return templates.TemplateResponse("/html/reconocimiento_facial.html", {"request": request})



known_encodings = []
known_names = []

# Función para cargar imágenes y crear encodings
def cargar_encodings():
    known_folder = "D:\SoftPython\python\static\conocidos"  # Carpeta donde se encuentran las imágenes de personas conocidas
    
    for filename in os.listdir(known_folder):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            image_path = os.path.join(known_folder, filename)
            image = face_recognition.load_image_file(image_path)
            encoding = face_recognition.face_encodings(image)[0]
            known_encodings.append(encoding)
            known_names.append(os.path.splitext(filename)[0])

cargar_encodings()

# Ruta para mostrar la página de registro de usuario
@appr.get("/registro_usuario", response_class=HTMLResponse)
async def registro_usuario_page(request: Request):
    return templates.TemplateResponse("/html/registro_usuario.html", {"request": request})

# Ruta para manejar el registro de usuario con reconocimiento facial
@appr.post("/registro_usuario")
async def registro_usuario(request: Request, nombre: str = Form(...), correo: str = Form(...), foto: UploadFile = Form(...)):
    # Obtener la imagen binaria de la foto
    foto_bytes = await foto.read()

    # Convertir la imagen en un array de numpy
    foto_image = PIL.Image.open(io.BytesIO(foto_bytes)).convert("RGB")
    foto_array = np.array(foto_image)

    # Detectar caras en la imagen
    face_locations = face_recognition.face_locations(foto_array)
    
    if len(face_locations) > 0:
        # Si se detecta al menos una cara, obtener la codificación de la primera cara
        foto_encoding = face_recognition.face_encodings(foto_array, face_locations)[0]
        
        # Resto del código para el registro y verificación
        # ...
        
        # Crear una carpeta con el nombre del usuario y guardar la foto
        user_folder = f"D:/SoftPython/python/static/usuarios/{nombre}"
        os.makedirs(user_folder, exist_ok=True)
        foto_path = f"{user_folder}/foto.jpg"
        with open(foto_path, "wb") as f:
            f.write(foto_bytes)
        print("fue bien")
        #return templates.TemplateResponse("/html/registro_usuario.html", {"request": request, "message": "Registro exitoso"})
        return {"success": True, "message": "Registro exitoso"}
    else:
        print("fue mal")
        #return templates.TemplateResponse("/html/registro_usuario.html", {"request": request, "error_message": "No se detectaron caras en la foto"})
        return {"success": False, "error_message": "No se detectaron caras en la foto"}


if __name__=='__main__':
   
    uvicorn.run(appr, host="localhost", port=8080)

 

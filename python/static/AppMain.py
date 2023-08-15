import subprocess
from fastapi import APIRouter #Importar modulo
import uvicorn #importar
from fastapi import Request, FastAPI, Form
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from funcion_insertar import *
from funcion_select import *
from funcion_update import *
import cv2
import face_recognition
import numpy as np
from pyzbar import pyzbar

from fastapi import FastAPI, File, UploadFile, Form, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os

import io
import os
import PIL.Image

from typing import List


appr = FastAPI()
"""
subprocess.run(
    [
        "openssl",
        "req",
        "-x509",
        "-newkey", "rsa:4096",
        "-keyout", "clave_privada.key",
        "-out", "certificado.crt",
        "-days", "365",
        "-subj", "/CN=localhost",  # Cambia "localhost" por el nombre de tu dominio
    ],
    check=True,
)"""

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
""""
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
    """



def generate_facial_frames():
    reference_folder = "D:/SoftPython/python/static/usuarios"
    reference_encodings = {}  # Usaremos un diccionario para mapear encodings a nombres de subcarpetas

    for folder_name in os.listdir(reference_folder):
        folder_path = os.path.join(reference_folder, folder_name)
        if os.path.isdir(folder_path):
            for image_name in os.listdir(folder_path):
                if image_name.lower().endswith(('.jpg', '.jpeg', '.png')):
                    image_path = os.path.join(folder_path, image_name)
                    reference_image = face_recognition.load_image_file(image_path)
                    reference_face_encoding = face_recognition.face_encodings(reference_image)[0]
                    reference_encodings[reference_face_encoding.tobytes()] = folder_name

    #camera = cv2.VideoCapture('http://172.24.216.1:8008/video')
    camera = cv2.VideoCapture(0)
    while True:
        ret, frame = camera.read()

        if not ret:
            break

        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)

        for face_encoding in face_encodings:
            matches = [face_recognition.compare_faces([np.frombuffer(encoding)], face_encoding)[0] for encoding in reference_encodings.keys()]
            if any(matches):
                matched_encoding = list(reference_encodings.keys())[matches.index(True)]
                name = reference_encodings[matched_encoding]
            else:
                name = "Desconocido"

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


# Ruta para mostrar la página de registro de usuario
@appr.get("/registro_usuario", response_class=HTMLResponse)
async def registro_usuario_page(request: Request):
    return templates.TemplateResponse("/html/registro_usuario.html", {"request": request})

# Ruta para manejar el registro de usuario con reconocimiento facial



@appr.post("/registro_usuario")
async def registro_usuario(nombre: str = Form(...), correo: str = Form(...), fotos: List[UploadFile] = File(...)):
    user_folder = f"python/static/usuarios/{nombre}"
    os.makedirs(user_folder, exist_ok=True)
    
    success_messages = []  # Lista para almacenar mensajes de éxito para cada foto
    error_messages = []    # Lista para almacenar mensajes de error para cada foto
    
    for i, foto in enumerate(fotos):
        foto_bytes = await foto.read()

        foto_image = PIL.Image.open(io.BytesIO(foto_bytes)).convert("RGB")
        foto_array = np.array(foto_image)

        face_locations = face_recognition.face_locations(foto_array)
        
        if len(face_locations) > 0:
            # Resto del código para el registro y verificación
            # ...

            foto_path = f"{user_folder}/foto_{i}.jpg"
            with open(foto_path, "wb") as f:
                f.write(foto_bytes)
            success_messages.append(f"Foto {foto.filename} registrada exitosamente")
        else:
            error_messages.append(f"No se detectaron caras en la foto {foto.filename}")

    if success_messages:
        return {"success": True, "message": " ".join(success_messages)}
    else:
        return {"success": False, "error_message": " ".join(error_messages)}

@appr.post("/update_correo")
async def update_correo(request: Request, nombre: str = Form(...), nuevo_correo: str = Form(...)):

    print(nombre)
    print(nuevo_correo)


    actualizarcorreowherenombre(nombre, nuevo_correo)
    

    
    return templates.TemplateResponse("/html/confirmacion_actualizacion.html", {"request": request, "nombre": nombre, "nuevo_correo": nuevo_correo})




if __name__=='__main__':
   
    uvicorn.run(appr, host="192.168.249.11", port=8081, 
                ssl_keyfile="clave_privada.key",
                ssl_certfile="certificado.crt",
                ssl_keyfile_password="1234")
 

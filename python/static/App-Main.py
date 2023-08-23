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
from funzbar import *
from fastapi import FastAPI, File, UploadFile, Form, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import io
import os
import PIL.Image
from typing import List
import json
import concurrent.futures

appr = FastAPI()
templates = Jinja2Templates(directory='D:\SoftPython\python\static')
appr.mount("/static", StaticFiles(directory="D:/SoftPython/python/static"), name="static")

@appr.get("/")
async def home(request: Request):
    return templates.TemplateResponse("/index.html", {"request": request})

@appr.post("/login")
def form_post(request: Request, eml: str = Form(...), psw: str = Form(...)):
    print(eml)
    print(psw)
    s = select_login(eml)
    print(s)
    return templates.TemplateResponse("/index.html", {"request": request})

@appr.post("/signup")
def form_post(request: Request, fn: str = Form(...), eml: str = Form(...), psw: str = Form(...), rpsw: str = Form(...)):
    print(fn)
    print(eml)
    print(psw)
    print(rpsw)
    insert_varibles_into_signup(fn, eml, psw, rpsw)
    return templates.TemplateResponse("/index.html", {"request": request})

@appr.get("/obtenerusr")
def homeusr(request: Request, eml: str):
    print(eml)
    print("obtener")
    s = select_login(eml)
    datos = {
        'titulo': 'Mi página',
        'mensaje': '¡Hola desde un endpoint!',
        'Correo': s[0][0],
        'Password': s[0][1]
    }
    return templates.TemplateResponse("/html/usuarios.html", {"request": request, "datos": datos})

@appr.get("/video_feed")
async def video_feed():
    return StreamingResponse(generate_frames(), media_type="multipart/x-mixed-replace; boundary=frame")

@appr.get("/obtenervideo")
async def obtener_video(request: Request):
    return templates.TemplateResponse("/html/obtener_video.html", {"request": request})

async def generate_facial_frames():
    reference_folder = "D:/SoftPython/python/static/usuarios"
    reference_encodings = {}

    print("Cargando encodings...")

    with concurrent.futures.ThreadPoolExecutor() as executor:
        folder_paths = [os.path.join(reference_folder, name) for name in os.listdir(reference_folder) if os.path.isdir(os.path.join(reference_folder, name))]

        for folder_path in folder_paths:
            folder_name = os.path.basename(folder_path)  
            future = executor.submit(load_reference_encodings, folder_path)
            encodings = future.result()
            print(f"Usuario: {folder_name}, encodings: {len(encodings)}")
            reference_encodings.update(encodings)

    print("Done.")

    camera = cv2.VideoCapture(0)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    camera.set(cv2.CAP_PROP_FPS, 50)

    while True:
        ret, frame = camera.read()

        if not ret:
            break

        face_locations = face_recognition.face_locations(frame, model='cnn')
        face_encodings = face_recognition.face_encodings(frame, face_locations)

        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(list(reference_encodings.keys()), face_encoding, tolerance=0.8)
            name = "Desconocido"

            if True in matches:
                matched_encoding = list(reference_encodings.keys())[matches.index(True)]
                path = reference_encodings[matched_encoding]
                name = os.path.basename(path)

            for (top, right, bottom, left) in face_locations:
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)

            _, buffer = cv2.imencode('.jpg', frame)
            frame_bytes = buffer.tobytes()

            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

    camera.release()
    
def load_reference_encodings(folder_path):

  encodings = {}

  for file_name in os.listdir(folder_path):

    if file_name.endswith(".json"):
        
      file_path = os.path.join(folder_path, file_name)
      
      with open(file_path) as f:
      
        data = json.load(f)
        
        encoding = tuple(data)
        
        encodings[encoding] = folder_path
        
  return encodings

@appr.get("/video_feed_facial")
async def video_feed_facial():
    return StreamingResponse(generate_facial_frames(), media_type="multipart/x-mixed-replace; boundary=frame")

@appr.get("/reconocimiento_facial_page")
async def reconocimiento_facial_page(request: Request):
    return templates.TemplateResponse("/html/reconocimiento_facial.html", {"request": request})

@appr.get("/registro_usuario", response_class=HTMLResponse)
async def registro_usuario_page(request: Request):
    return templates.TemplateResponse("/html/registro_usuario.html", {"request": request})

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
            # Generar encodings faciales
            face_encodings = face_recognition.face_encodings(foto_array, face_locations)
            
            if face_encodings:
                # Almacenar encoding en un archivo
                for j, encoding in enumerate(face_encodings):
                    encoding_path = f"{user_folder}/encoding_{i}_{j}.json"
                    with open(encoding_path, "w") as encoding_file:
                        json.dump(encoding.tolist(), encoding_file)
                
                foto_path = f"{user_folder}/foto_{i}.jpg"
                with open(foto_path, "wb") as f:
                    f.write(foto_bytes)
                success_messages.append(f"Foto {foto.filename} registrada exitosamente")
            else:
                error_messages.append(f"No se pudieron generar encodings para la foto {foto.filename}")
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
   
    uvicorn.run(appr, host="localhost", port=8081, 
                ssl_keyfile="clave_privada.key",
                ssl_certfile="certificado.crt",
                ssl_keyfile_password="1234")
 

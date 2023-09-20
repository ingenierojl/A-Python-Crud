from fastapi import APIRouter
import uvicorn
from fastapi import Request, FastAPI, Form, UploadFile, File
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from py.funcion_insertar import *
from py.funcion_select import *
from py.funcion_update import *
from py.funzbar import *
import face_recognition
import numpy as np
import os
import io
import PIL.Image
from typing import List
import json
import concurrent.futures
from fastapi import FastAPI, Depends, HTTPException 
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError


#import fingerprint


#import pycuda.driver as cuda
#import pycuda.autoinit
#ctx = cuda.Context.get_device() 

# Código para ejecutar kernels CUDA

appr = FastAPI()

templates = Jinja2Templates(directory='D:\SoftPython\python\static')
appr.mount("/static", StaticFiles(directory="D:/SoftPython/python/static"), name="static")

@appr.get("/")
async def home(request: Request):
    return templates.TemplateResponse("/index.html", {"request": request})

"""
@appr.post("/login")
def form_post(request: Request, eml: str = Form(...), psw: str = Form(...)):
    s = select_login(eml)
    print(s[0][1])
    if (psw == s[0][1]):
        print ("clave correcta")
        return templates.TemplateResponse("/index.html", {"request": request})
    else:
        return "error"
"""

SECRET_KEY = "mi_clave_secreta" 
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
@appr.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):

    eml = form_data.username #debe llamarse en el input username alla en el email :/
    psw = form_data.password #name=password en el input por protocolo oath:/
    user = select_login(eml)
    print(user)
    print(psw)

    if psw == user[0][1]:
       token = jwt.encode({"sub": eml}, SECRET_KEY, algorithm="HS256")
       
       print("creado")
       print(token)
       return {"access_token": token, "token_type": "bearer"}

    return HTTPException(status_code=400, detail="Usuario o contraseña incorrectos")

@appr.post('/protected')
def protected_route(token: str = Depends(oauth2_scheme)):

  try:  
    print("payload")
    payload = jwt.decode(token, SECRET_KEY)
    print("acceso autorizado")
    return {"message": "Acceso autorizadoooo"}   
              
  except JWTError: 
    raise HTTPException(status_code=401, detail='Token inválido')

@appr.post("/signup")
def form_post(request: Request, fn: str = Form(...), eml: str = Form(...), psw: str = Form(...), rpsw: str = Form(...)):
    insert_varibles_into_signup(fn, eml, psw, rpsw)
    return templates.TemplateResponse("/index.html", {"request": request})

@appr.get("/obtenerusr")
def homeusr(request: Request, eml: str):
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
    try:
        return StreamingResponse(generate_frames(), media_type="multipart/x-mixed-replace; boundary=frame")
    except:
        print("no se pudo zbar")
@appr.get("/obtenervideo")
async def obtener_video(request: Request):
    return templates.TemplateResponse("/html/obtener_video.html", {"request": request})


model = 'hog'
num_jitters = 2
tolerance = 0.45
ancho=720
alto=720
fps=30

#face_recognition.cuda = True

async def generate_facial_frames():
    reference_folder = "D:/SoftPython/python/static/usuarios"
    print("Cargando encodings de referencia...")
    reference_encodings, user_encoding_counts = load_all_reference_encodings(reference_folder)
    
    for user, count in user_encoding_counts.items():
        print(f"{user} tiene {count} encodings")

    camera = cv2.VideoCapture(2)

    try:
        camera.set(cv2.CAP_PROP_FRAME_WIDTH, ancho)
        camera.set(cv2.CAP_PROP_FRAME_HEIGHT, alto)
        camera.set(cv2.CAP_PROP_FPS, fps)

        while True:
            ret, frame = camera.read()

            if not ret:
                break

            small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)

            face_locations = face_recognition.face_locations(small_frame, model=model)
            face_encodings = face_recognition.face_encodings(small_frame, face_locations, num_jitters=num_jitters)

            
    

            names = []

            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(list(reference_encodings.keys()), face_encoding, tolerance=tolerance)
                name = "Desconocido"

                if True in matches:
                    matched_idx = matches.index(True)
                    encoding_key = list(reference_encodings.keys())[matched_idx]
                    name = reference_encodings[encoding_key]

                names.append(name)

            for (top, right, bottom, left), name in zip(face_locations, names):
                top *= 2
                right *= 2
                bottom *= 2
                left *= 2

                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

            _, buffer = cv2.imencode('.jpg', frame)
            frame_bytes = buffer.tobytes()
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

    finally:
        camera.release()

def load_all_reference_encodings(reference_folder):
    reference_encodings = {}
    user_encoding_counts = {}

    with concurrent.futures.ThreadPoolExecutor() as executor:
        folder_paths = [os.path.join(reference_folder, f) for f in os.listdir(reference_folder) if os.path.isdir(os.path.join(reference_folder, f))]
        futures = [executor.submit(load_reference_encodings, folder_path, os.path.basename(folder_path)) for folder_path in folder_paths]

        for future in concurrent.futures.as_completed(futures):
            encodings = future.result()
            reference_encodings.update(encodings)
            user_name = os.path.basename(folder_paths[futures.index(future)])
            user_encoding_counts[user_name] = len(encodings)

    return reference_encodings, user_encoding_counts


def load_reference_encodings(folder_path, folder_name):

  encodings = {}

  for file_name in os.listdir(folder_path):

    if file_name.endswith(".json"):
      
      path = os.path.join(folder_path, file_name)

      with open(path) as f:
         data = json.load(f)
         encodings[tuple(data)] = folder_name

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
    
    success_messages = []
    error_messages = []
    
    for i, foto in enumerate(fotos):
        foto_bytes = await foto.read()

        foto_image = PIL.Image.open(io.BytesIO(foto_bytes)).convert("RGB")
        foto_array = np.array(foto_image)

        face_locations = face_recognition.face_locations(foto_array)
        
        if len(face_locations) > 0:
            face_encodings = face_recognition.face_encodings(foto_array, face_locations)
            
            if face_encodings:
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
    actualizarcorreowherenombre(nombre, nuevo_correo)
    return templates.TemplateResponse("/html/confirmacion_actualizacion.html", {"request": request, "nombre": nombre, "nuevo_correo": nuevo_correo})
if __name__ == '__main__':
    uvicorn.run(appr, host="localhost", port=8082)

"""
if __name__ == '__main__':
    uvicorn.run(appr, host="localhost", port=8081, 
                ssl_keyfile="clave_privada.key",
                ssl_certfile="certificado.crt",
                ssl_keyfile_password="1234")
"""
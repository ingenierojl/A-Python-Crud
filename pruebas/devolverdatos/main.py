from fastapi import FastAPI, Request
#from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import uvicorn

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/")
async def home(request: Request):
    datos = {
        'titulo': 'Mi página',
        'mensaje': '¡Hola desde Python!',
        'nombre': 'Juan',
        'edad': 30
    }
    return templates.TemplateResponse("index.html", {"request": request, "datos": datos})


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)

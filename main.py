from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
from typing import List

from utilGrafo import cargar_grafo, cargar_grafo_cytoscape, POSICIONES_NODOS
from ba import ba_horario, ba_antihorario
from bp import bp_horario, bp_antihorario
from es import es_horario, es_antihorario
from pm import pm_horario, pm_antihorario

app = FastAPI()
# Servir archivos estáticos (CSS, JS, imágenes)
app.mount("/static", StaticFiles(directory="static"), name="static")
# Configurar motor de plantillas
templates = Jinja2Templates(directory="templates")

# Cargar el grafo desde el archivo JSON al iniciar la aplicación
mi_grafo = cargar_grafo("grafo.json")

# Modelo de datos que envía el frontend al presionar "Buscar"
class BusquedaRequest(BaseModel):
    algoritmo: str
    sentido: str
    inicio: int = Field(..., ge=1, le=28)
    fin: int = Field(..., ge=1, le=28)

# Mapa de algoritmos disponibles
MAPA_BUSQUEDAS = {
    ("ancho", "horario"): ba_horario,
    ("ancho", "antihorario"): ba_antihorario,
    ("profundidad", "horario"): bp_horario,
    ("profundidad", "antihorario"): bp_antihorario,
    ("escalada", "horario"): es_horario,
    ("escalada", "antihorario"): es_antihorario,
    ("primero_mejor", "horario"): pm_horario,
    ("primero_mejor", "antihorario"): pm_antihorario,
}

@app.get("/api/grafo")
async def obtener_grafo():
    # Retorna la lista de nodos con posiciones y aristas con pesos
    return cargar_grafo_cytoscape("grafo.json", POSICIONES_NODOS)

@app.post("/api/buscar")
async def resolver_busqueda(request: BusquedaRequest):
    clave = (request.algoritmo, request.sentido)

    # Buscar la función correspondiente en el mapa
    funcion_busqueda = MAPA_BUSQUEDAS.get(clave)

    if funcion_busqueda:
        ruta, lista_pasos = funcion_busqueda(mi_grafo, request.inicio, request.fin)
    else:
        ruta = None
        lista_pasos = f"Método {request.algoritmo} ({request.sentido}) no disponible."
    
    return {
        "ruta": ruta,
        "pasos": lista_pasos
    }

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")
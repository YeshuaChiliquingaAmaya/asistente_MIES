# scraper_duplicado_cedula.py
# Extrae la información del trámite "Emisión de duplicado de cédula de identidad" desde gob.ec

import requests
from bs4 import BeautifulSoup
import json

BASE_URL = "https://www.gob.ec"
LIST_URL = f"{BASE_URL}/tramites/lista"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

TRAMITE_BUSCADO = "Emisión de duplicado de cédula de identidad"


def buscar_url_tramite():
    """Busca la URL del trámite específico en la lista de trámites."""
    page = 0
    while True:
        url = f"{LIST_URL}?page={page}"
        resp = requests.get(url, headers=HEADERS, timeout=20)
        soup = BeautifulSoup(resp.content, 'html.parser')
        links = soup.select('h3.field-content a, div.listing-boxes-text h3 a')
        if not links:
            break
        for link in links:
            if TRAMITE_BUSCADO.lower() in link.get_text(strip=True).lower():
                return BASE_URL + link['href']
        page += 1
    return None

def extraer_detalles_tramite(tramite_url):
    resp = requests.get(tramite_url, headers=HEADERS, timeout=20)
    soup = BeautifulSoup(resp.content, 'html.parser')
    def get_text_safely(selector):
        el = soup.select_one(selector)
        return el.get_text(strip=True) if el else "No disponible"
    tramite_data = {
        "Nombre_Tramite": get_text_safely("h1.page-header"),
        "Institucion_Responsable": get_text_safely("div.alert-info a"),
        "URL_Fuente": tramite_url,
        "Descripcion": get_text_safely("div#description"),
    }
    return tramite_data

if __name__ == "__main__":
    print(f"Buscando trámite: {TRAMITE_BUSCADO}")
    tramite_url = buscar_url_tramite()
    if tramite_url:
        print(f"URL encontrada: {tramite_url}")
        detalles = extraer_detalles_tramite(tramite_url)
        with open("tramite_duplicado_cedula.json", "w", encoding="utf-8") as f:
            json.dump(detalles, f, ensure_ascii=False, indent=4)
        print("Detalles guardados en tramite_duplicado_cedula.json")
    else:
        print("No se encontró el trámite solicitado.")

# Persistencia de datos de archivos
from pathlib import Path
import json
import csv

# Carpeta data relativa al proyecto
DATA_DIR = Path(__file__).parent.parent / "data"

TXT_FILE = DATA_DIR / "datos.txt"
JSON_FILE = DATA_DIR / "datos.json"
CSV_FILE = DATA_DIR / "datos.csv"

# --- TXT ---
def guardar_txt(producto: dict):
    with open(TXT_FILE, "a", encoding="utf-8") as f:
        f.write(f"{producto['nombre']},{producto['cantidad']},{producto['precio']}\n")

def leer_txt():
    productos = []
    if TXT_FILE.exists():
        with open(TXT_FILE, "r", encoding="utf-8") as f:
            for linea in f:
                nombre, cantidad, precio = linea.strip().split(",")
                productos.append({"nombre": nombre, "cantidad": cantidad, "precio": precio})
    return productos


# --- JSON ---
def guardar_json(producto: dict):
    data = []
    if JSON_FILE.exists() and JSON_FILE.stat().st_size > 0:
        with open(JSON_FILE, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []  # si hay error, reinicia la lista
    data.append(producto)
    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def leer_json():
    if JSON_FILE.exists() and JSON_FILE.stat().st_size > 0:  # archivo existe y no está vacío
        with open(JSON_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []  # si está vacío, devuelve lista vacía



# --- CSV ---
def guardar_csv(producto: dict):
    with open(CSV_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["nombre", "cantidad", "precio"])
        if f.tell() == 0:  # si el archivo está vacío, escribir cabecera
            writer.writeheader()
        writer.writerow(producto)

def leer_csv():
    productos = []
    if CSV_FILE.exists():
        with open(CSV_FILE, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                productos.append({"nombre": row["nombre"], "cantidad": row["cantidad"], "precio": row["precio"]})
    return productos

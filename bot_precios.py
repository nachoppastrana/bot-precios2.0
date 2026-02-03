import asyncio
import json
import os
import requests
from bs4 import BeautifulSoup
from telegram import Bot

import os

TOKEN = os.getenv["8317818913:AAGe8JbLfFFDucXBDGWMwapmh2Ly6FGE4b4"]
CHAT_ID = os.getenv["1134808904"]


URL = "https://listado.mercadolibre.com.ar/zapatillas-adidas"

ARCHIVO = "precios.json"
PRECIO_OBJETIVO = 100000

def obtener_precio():
    r = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(r.text, "html.parser")

    precio = soup.find("span", class_="andes-money-amount__fraction")
    if not precio:
        return None

    return int(precio.text.replace(".", ""))

def cargar_precio():
    if not os.path.exists(ARCHIVO):
        return None
    with open(ARCHIVO, "r") as f:
        return json.load(f).get("precio")

def guardar_precio(p):
    with open(ARCHIVO, "w") as f:
        json.dump({"precio": p}, f)

async def main():
    bot = Bot(token=TOKEN)

    await bot.send_message(
        chat_id=CHAT_ID,
        text="🧪 Bot de precios ejecutándose correctamente"
    )

    nuevo = obtener_precio()
    viejo = cargar_precio()

    if nuevo is None:
        return

    if viejo is None:
        guardar_precio(nuevo)
        await bot.send_message(
            chat_id=CHAT_ID,
            text=f"👀 Precio registrado\nActual: ${nuevo}"
        )
        return

    if nuevo <= PRECIO_OBJETIVO and nuevo != viejo:

        guardar_precio(nuevo)
        await bot.send_message(
            chat_id=CHAT_ID,
            text=f"🔥 Cambio de precio detectado\nAntes: ${viejo}\nAhora: ${nuevo}"
        )

import time

if __name__ == "__main__":
        asyncio.run(main())



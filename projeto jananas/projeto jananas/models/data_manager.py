import os
import json
import config
import requests
import random


def save_data(cadastro):
    with open(config.DATA_FILE, "w") as file:
        json.dump(cadastro, file, indent=4)

def load_data():
    if not os.path.exists(config.DATA_FILE):
        return [ ]
    with open(config.DATA_FILE, "r") as file:
        return (json.load(file))

def quote_get():
    quotes = []
    resp = requests.get("https://type.fit/api/quotes")
    dados = resp.json()
    for i in range(20):  
        quote = random.choice(dados)["text"]
        quotes.append(quote)
    return quotes

def save_info(info):
    with open(config.FOTOS_FILE, "w") as file:
        json.dump(info, file, indent=4)

def load_info():
    if not os.path.exists(config.FOTOS_FILE):
        return [ ]
    with open(config.FOTOS_FILE, "r") as file:
        return (json.load(file))
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
    url = "https://api.api-ninjas.com/v1/loremipsum?paragraphs=1&max_length=10"
    headers = {"X-Api-Key": "zp6GyOGDnj0Ku8A7n8msdQ==a8vTfXQGIvx6KKEx"}
    resp = requests.get(url,headers=headers)
    
    dados = resp.json()
    text = dados["text"]
    for i in range(20):  
        quotes.append(text)
    return quotes

def save_info(info):
    with open(config.FOTOS_FILE, "w") as file:
        json.dump(info, file, indent=4)

def load_info():
    if not os.path.exists(config.FOTOS_FILE):
        return [ ]
    with open(config.FOTOS_FILE, "r") as file:
        return (json.load(file))

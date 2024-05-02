from fastapi import FastAPI
import json
from pathlib import Path
from transformers import pipeline
import requests
from PIL import Image
from tensorflow.keras.applications import EfficientNetB0
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.efficientnet import preprocess_input
from tensorflow.keras.applications.efficientnet import decode_predictions
import numpy as np

DATAFILE_CONTENT = {"url1" : ["streetcar 0.74", 
                              "passenger_car 0.23", "electric_locomotive 0.02"]}
DATAFILE_PATH = Path("./base.json")

def datafile_load():
    global DATAFILE_CONTENT
    global DATAFILE_PATH
    if DATAFILE_PATH.is_file():
        with open(DATAFILE_PATH, 'r') as f:
            DATAFILE_CONTENT = json.load(f)
    else:
        with open(DATAFILE_PATH, "w") as f:
            f.write(json.dumps(DATAFILE_CONTENT, sort_keys=True, indent=4))
        with open(DATAFILE_PATH, 'r') as f:
            DATAFILE_CONTENT = json.load(f)

# Загружаем предварительно обученную модель EfficientNetB0
model = EfficientNetB0(weights='imagenet')

def recognition_img(url):
    # Указываем путь к файлу с изображением, 
    # который будем использовать для сохранения файла и его использования
    img_path = 'image.jpg'
    # Сохраняем JPG из полученного в запросе URL
    img = Image.open(requests.get(url, stream = True).raw)
    img.save(img_path)

    # Загружаем изображение в память. 
    # EfficientNetB0 рассчитана на изображения размером 224х224
    img = image.load_img(img_path, target_size=(224, 224))
    # Выполняем предварительную обработку изображения
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    # Запускаем распознавание
    preds = model.predict(x)
    # СО=оставляем строку с ТОП-3 классами с самой большой вероятностью
    classes = decode_predictions(preds, top=3)[0]
    res = 'Results:'
    for cl in classes:
        res = res + ' ' + cl[1] + ' ' + str(round(cl[2], 2)) + ';'
    # Возвращаем строку
    return res[:-1]

def result_to_array(str):
    x = str.split("; ")
    return x

def set_new_record(url):
    global DATAFILE_CONTENT
    global DATAFILE_PATH

    datafile_load()

    with open(DATAFILE_PATH, 'r+') as f:
        DATAFILE_CONTENT = json.load(f)
        DATAFILE_CONTENT[url] = result_to_array(recognition_img(url)[9:])
        f.seek(0)
        f.write(json.dumps(DATAFILE_CONTENT, sort_keys=True, indent=4))
        f.truncate()
    print("Data:")
    print(DATAFILE_CONTENT)
    # Запись нового Json в файл
    return DATAFILE_CONTENT

def print_answer(url):
    global DATAFILE_CONTENT
    datafile_load()
    if url in DATAFILE_CONTENT:
        return "This image was recognize.Result - " + \
            DATAFILE_CONTENT[url][0] + "; " + \
            DATAFILE_CONTENT[url][1] + "; " + \
            DATAFILE_CONTENT[url][2] + "."
    else:
        if check_is_image(url):
            set_new_record(url)
            return "Image recognizing... Result - " + \
            DATAFILE_CONTENT[url][0] + "; " + \
            DATAFILE_CONTENT[url][1] + "; " + \
            DATAFILE_CONTENT[url][2] + "."
        else:
            return "This is not image."

def check_is_image(url):
    try:
        Image.open(requests.get(url, stream=True).raw)
        return True
    except:
        return False

app = FastAPI()
classifier = pipeline("sentiment-analysis")

# Сообщение-заглушка для метода GET с инструкцией для метода POST
@app.get("/")
def get_root():
    return {"message": "Use POST + url to JPG image for recognition."}

# Метод GET для получения базы распознаных изображений
@app.get("/base/")
def get_base():
    datafile_load()
    return DATAFILE_CONTENT

# Метод POST для корня
@app.post("/")
def post_root(url: str):
    # Запускаем функцию recognition_img ,
    # передавая URL JPG картинки из запроса. 
    # Возвращаем строку с ТОП-3 классами, которые определила модель
    return print_answer(url)
    # return recognition_img(url)

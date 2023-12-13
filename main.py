from transformers import pipeline
import requests
from PIL import Image
from tensorflow.keras.applications import EfficientNetB0
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.efficientnet import preprocess_input
from tensorflow.keras.applications.efficientnet import decode_predictions
import numpy as np
from fastapi import FastAPI

# def recognition(img_path):

# Загружаем предварительно обученную модель EfficientNetB0
model = EfficientNetB0(weights='imagenet')

def recognition_img(url):
    # Указываем путь к файлу с изображением, который будем использовать для сохранения файла и его использования
    img_path = 'image.jpg'
    # Сохраняем JPG из полученного в запросе URL
    img = Image.open(requests.get(url, stream = True).raw)
    img.save(img_path)

    # Загружаем изображение в память. EfficientNetB0 рассчитана на изображения размером 224х224
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

#Из библиотеки fastAPI воспользуемся методом для анализа настроений
app = FastAPI()
classifier = pipeline("sentiment-analysis")

# Методы
# Сообщение-заглушка для метода GET с инструкцией для метода POST
@app.get("/")
def getRoot():
    return {"message": "Use POST + url to JPG image for recognition."}
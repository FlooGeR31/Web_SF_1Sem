# API приложение
Распознаёт объект на изображении с переданным URL/

## Содержание
- [ВОзможности](#возможности)
- [Технологии](#технологии)
- [Использование](#использование)
- [Цель проекта](#цель-проекта)
- [Команда проекта](#команда-проекта)
- [Источники](#источники)

## Возможности
- На запрос POST в корень с URL JPG картинки возвращает ТОП-3 класса с наибольшей вероятностью по результатам распознавания моделью EfficientNetB0.
- Если отправленный URL уже был ранее использован, то данные распознавания будут взяты из файла с сохранёнными результатами распознавания.
- Если отправленный URL ранее не был распознан, то кроме отправки результата в ответе результат сохраняется в файл с результатами.
- На запрос GET в /base/ приложение вернёт всё содержимое файла с сохранёнными результатами распознавания.
- Если в запросе POST в корень передан url НЕ изображения, то придёт соответствующий ответ.

## Технологии
- [Python](https://www.python.org/)
- [TensorFlow](https://www.tensorflow.org/?hl=ru)
- [HTTP](https://developer.mozilla.org/ru/docs/Web/HTTP/Overview)
- [Pytest](https://docs.pytest.org/en/7.4.x/)

## Использование
- Установите зависимости:
```
pip install -r requirements.txt
```
- Запустите приложение:
```
uvicorn se_hw3_api:app
```
- Отправьте запрос POST с URL JPG картинки, например:
```
curl -X 'POST' \
  'http://127.0.0.1:8000/?url=https%3A%2F%2Fpilotinstitute.com%2Fwp-content%2Fuploads%2F2023%2F02%2FHow-Much-Do-Airplanes-Cost.jpg' \
  -H 'accept: application/json' \
  -d ''
```
или
```
curl -X 'POST' \
  'http://127.0.0.1:8000/?url=https%3A%2F%2Fimg.freepik.com%2Ffree-photo%2Fsteam-train-chugs-through-mountain-forest-scene-generative-ai_188544-8072.jpg' \
  -H 'accept: application/json' \
  -d ''
```
- Также для отправки запросов и просмотра ответов можно использовать интерфейс FastAPI по адресу http://127.0.0.1:8000/docs

## Цель проекта
Практика в разработке API приложения.

## Команда проекта
Контакты и инструкции, как связаться с командой разработки.

- [Александр М.](tg://abc) — Developer
- [Сергей Г.](tg://abc) — Исследования, тестирование
- [Виталий К.](tg://abc) — Developer
- [Денис С.](tg://abc) — Developer, Орг. вопросы, оформление
- [Юлия](tg://abc) — Developer
- [Алёна](tg://abc) — Исследования, тестирование

## Источники
https://metanit.com/python/fastapi/1.10.php
https://habr.com/ru/articles/708678/
https://blog.finxter.com/5-easy-ways-to-download-an-image-from-a-url-in-python/
https://www.tensorflow.org/tutorials/load_data/images?hl=ru
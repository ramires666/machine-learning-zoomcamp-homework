#%%
import onnxruntime as ort
import numpy as np
import os
from keras_image_helper import create_preprocessor
import json


def preprocess_pytorch_style(X):
    # X: shape (1, 3, 299, 299, dtype=float32, values in [0, 255])
    # Эта строка была псевдокодом и вызывала ошибку синтаксиса. Я её закомментировал.
    # На вход мы получаем массив изображений (batch) от keras_image_helper.
    # Обычно это формат NHWC: (количество, высота, ширина, каналы).

    # 1. Приводим значения пикселей к диапазону [0, 1].
    # Изначально они от 0 до 255. Делим на 255.0, чтобы получить float.
    X = X / 255.0

    # 2. Задаем параметры нормализации (среднее и стандартное отклонение).
    # Эти числа — стандарт для моделей, обученных на ImageNet (как MobileNet, ResNet и др.).
    # Мы делаем reshape в (1, 3, 1, 1), чтобы эти массивы соответствовали формату NCHW (каналы на втором месте).
    mean = np.array([0.485, 0.456, 0.406], dtype=np.float32).reshape(1, 3, 1, 1)
    std = np.array([0.229, 0.224, 0.225], dtype=np.float32).reshape(1, 3, 1, 1)

    # Convert NHWC → NCHW
    # from (batch, height, width, channels) → (batch, channels, height, width)
    # 3. Меняем порядок осей (транспонируем).
    # PyTorch и ONNX любят, когда каналы (цвета) идут перед высотой и шириной.
    X = X.transpose(0, 3, 1, 2)

    # Normalize
    # 4. Нормализуем: вычитаем среднее и делим на разброс (стандартное отклонение).
    # Благодаря reshape выше, numpy понимает, как отнять (1,3,1,1) от (1,3,299,299).
    X = (X - mean) / std

    # Возвращаем результат, явно указывая тип float32 (это важно для ONNX Runtime).
    return X.astype(np.float32)


preprocessor = create_preprocessor(preprocess_pytorch_style, target_size=(224, 224))
# preprocessor = create_preprocessor("xception", target_size=(299, 299))

# Выносим имя модели в переменную окружения. Если переменной нет, берем дефолтное значение.
MODEL_NAME = os.getenv("MODEL_NAME", "clothing_classifier_mobilenet_v2_latest.onnx")

session = ort.InferenceSession(
    MODEL_NAME, providers=["CPUExecutionProvider"]
)
input_name = session.get_inputs()[0].name
output_name = session.get_outputs()[0].name

classes = [
    "dress",
    "hat",
    "longsleeve",
    "outwear",
    "pants",
    "shirt",
    "shoes",
    "shorts",
    "skirt",
    "t-shirt",
]


def predict(url):
    X = preprocessor.from_url(url)
    result = session.run([output_name], {input_name: X})
    float_predictions = result[0][0].tolist()
    d = dict(zip(classes, float_predictions))
    return sorted(d.items(), key=lambda kv: kv[1], reverse=True)

#%%
def lambda_handler(event, context):
    # Добавляем обработку ошибок, чтобы понимать, что пошло не так в логах AWS Lambda
    try:
        print(f"Received event: {event}") # Логируем входящее событие для дебага

        body = event.get("body") or "{}"
        data = json.loads(body) if isinstance(body, str) else body

        url = data.get("url")
        if not url:
            return {"statusCode": 400, "body": json.dumps("Error: URL is missing in the request body")}

        # url: "http://bit.ly/mlbookcamp-pants" <- Тоже закомментировал, это невалидный код
        print(f"Predicting for URL: {url}")

        result = predict(url)
        print(f"Prediction result: {result}")

        answer = f"So my guess is: its either a {result[0][0].upper()} or a {result[1][0].upper()} or maybe a {result[2][0].upper()}"

        return {
            "statusCode": 200,
            "headers": {"content-type": "application/json"},
            "body": json.dumps(answer)
        }
    except Exception as e:
        print(f"Error in lambda_handler: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
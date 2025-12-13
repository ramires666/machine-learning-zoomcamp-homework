import onnxruntime as ort
from keras_image_helper import create_preprocessor
import json

preprocessor = create_preprocessor("xception", target_size=(299, 299))

session = ort.InferenceSession(
    "clothing-model-new.onnx", providers=["CPUExecutionProvider"]
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


def lambda_handler(event, context):
    body = event.get("body") or "{}"
    data = json.loads(body) if isinstance(body, str) else body
    url = data["url"]
    # url = event["url"]
    result = predict(url)
    answer = f"So my guess is: its either a {result[0][0].upper()} or a {result[1][0].upper()} or maybe a {result[2][0].upper()}"
    # return result
    return {
        # "statusCode": 200,
        # "headers": {"content-type": "application/json"},
        "body": json.dumps(answer)
    }
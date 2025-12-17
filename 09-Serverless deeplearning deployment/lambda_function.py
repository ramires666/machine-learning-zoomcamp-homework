#%%
import onnxruntime as ort
import numpy as np
import json
from io import BytesIO
from urllib import request
from PIL import Image

def download_image(url):
    with request.urlopen(url) as resp:
        buffer = resp.read()
    stream = BytesIO(buffer)
    img = Image.open(stream)
    return img


def prepare_image(img, target_size):
    if img.mode != 'RGB':
        img = img.convert('RGB')
    img = img.resize(target_size, Image.NEAREST)
    return img


def preprocess(img, size=(200, 200), add_batch=True):
    MEAN = np.array([0.485, 0.456, 0.406], dtype=np.float32)  # RGB
    STD = np.array([0.229, 0.224, 0.225], dtype=np.float32)  # RGB

    # img = img.resize(size, resample=Image.BILINEAR)

    # ToTensor(): HWC uint8 -> float32 CHW в [0,1] [web:197]
    x = np.asarray(img, dtype=np.float32)  # (H,W,3), 0..255
    x = x / 255.0  # (H,W,3), 0..1
    x = np.transpose(x, (2, 0, 1))  # (3,H,W) = CHW

    # Normalize: (x - mean) / std
    x = (x - MEAN[:, None, None]) / STD[:, None, None]

    # Batch dimension = (tensor_img.unsqueeze(0))
    if add_batch:
        x = x[None, :, :, :]    # (1,3,H,W)

    return x.astype(np.float32)


def predict(url):
    img = download_image(url)
    img = prepare_image(img, target_size=(200, 200))
    X = preprocess(img)

    session = ort.InferenceSession("hair_classifier_empty.onnx", providers=["CPUExecutionProvider"])
    input_name = session.get_inputs()[0].name
    output_name = session.get_outputs()[0].name

    result = session.run([output_name], {input_name: X})
    return result[0][0][0]


#%%
## TESTING:
url = "https://habrastorage.org/webt/yf/_d/ok/yf_dokzqy3vcritme8ggnzqlvwa.jpeg"
# straight:
url = "https://www.indiquehair.com/cdn/shop/files/Indique_SEA_Bali_Straight.jpg?v=1756924716&width=1080"
url = "https://media.istockphoto.com/id/1697342572/photo/portrait-of-woman-with-perfect-long-straight-hair-in-a-natural-color-hairstyling-hair-care.jpg?s=612x612&w=0&k=20&c=RTl9HMCcWux7T-dtDGrnmnqbRCBszjHcZpRaAC_tocU="
url = "https://i.pinimg.com/736x/69/c0/d5/69c0d5b003952682ba5ff36d6527d84b.jpg"
url = "https://media.madison-reed.com/d3ewrnwdcmri66.cloudfront.net/content/images/2016/6/straighthair1/straighthair1-891x600.jpeg"
url = "https://cdn.shopify.com/s/files/1/0641/2831/9725/files/Blunt_bob_for_straight_hair_women.webp?v=1750312910"
url = 'https://img.wattpad.com/da171ffe58dbf5469ce46124f5582d3167e3db26/68747470733a2f2f73332e616d617a6f6e6177732e636f6d2f776174747061642d6d656469612d736572766963652f53746f7279496d6167652f4a6b4d726d526b41536f6a6d68513d3d2d34342e313664373065353361623135343564323338343234303232343334342e6a7067?s=fit&w=720&h=720'
# curly:
url = 'https://i.pinimg.com/564x/e3/8a/1b/e38a1ba3ea4a9eb91a8750145450a0ed.jpg'
url = 'https://live-essnc.s3.amazonaws.com/uploads/2024/06/41261604_238083550389311_2718376404700889088_n.jpg'
url = 'https://curlmaven.ie/wp-content/uploads/2021/01/how-to-build-a-curly-hair-routine-feature-image-768x1152.jpg'
url = 'https://edwardsandcoeducation.com/wp-content/uploads/2020/12/Screen-Shot-2020-12-18-at-5.00.58-pm.jpg'


def lambda_handler(event, context):
    try:
        print(f"Received event: {event}")

        body = event.get("body") or "{}"
        data = json.loads(body) if isinstance(body, str) else body

        # url = event.get("url")
        url = data.get("url")
        if not url:
            return {"statusCode": 400, "body": json.dumps("Error: URL is missing in the request body")}

        print(f"Predicting for URL: {url}")

        result = predict(url).item()
        print(f"Prediction result: {result}")

        return {
            "statusCode": 200,
            "headers": {"content-type": "application/json"},
            "body": json.dumps(result)
        }
    except Exception as e:
        print(f"Error in lambda_handler: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
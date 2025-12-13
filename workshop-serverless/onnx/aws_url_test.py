import requests
import json

url = "https://hw4m3f7n5abdudfdweh3hix4j40lfdno.lambda-url.ap-northeast-1.on.aws/"

TPyXAHbI = "https://cdn11.bigcommerce.com/s-b1nxqcmq/images/stencil/760x760/products/550/4152/Oxford_Button_Down_Shirt_Lt._Blue__27710.1762839125.png?c=2"
payload = {"url":TPyXAHbI}

r = requests.post(url, json=payload, timeout=30)

print(json.loads(r.text)['body'])

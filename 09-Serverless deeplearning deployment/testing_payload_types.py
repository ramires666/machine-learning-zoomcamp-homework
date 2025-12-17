import requests
import json

url = "https://wn6ody7cdu4fhtwkvnxn5r6f5i0palgh.lambda-url.ap-northeast-1.on.aws/"

payload = {
    "url": "https://habrastorage.org/webt/yf/_d/ok/yf_dokzqy3vcritme8ggnzqlvwa.jpeg"
}

print("Тест 1: Стандартный запрос")
r1 = requests.post(url, json=payload)
print(f"Статус: {r1.status_code}")
print(f"Ответ: {r1.text}\n")

print("Тест 2: С явным Content-Type")
r2 = requests.post(
    url,
    json=payload,
    headers={"Content-Type": "application/json"}
)
print(f"Статус: {r2.status_code}")
print(f"Ответ: {r2.text}\n")

print("Тест 3: Передача data вместо json")
r3 = requests.post(
    url,
    data=json.dumps(payload),
    headers={"Content-Type": "application/json"}
)
print(f"Статус: {r3.status_code}")
print(f"Ответ: {r3.text}")

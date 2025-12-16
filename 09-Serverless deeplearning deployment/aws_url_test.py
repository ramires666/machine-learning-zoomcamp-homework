import requests
import json

url = "https://kusxrpivnyetqmjzzvxm32kfvy0ntrkh.lambda-url.ap-northeast-1.on.aws/"


hairy_potter = "https://habrastorage.org/webt/yf/_d/ok/yf_dokzqy3vcritme8ggnzqlvwa.jpeg"
payload = {"url":hairy_potter}

r = requests.post(url, json=payload, timeout=30)

print(json.loads(r.text))

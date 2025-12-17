

import requests
import json

url = "https://u6xla0ww35.execute-api.ap-northeast-1.amazonaws.com/test1/predict"


hairy_potter = "https://habrastorage.org/webt/yf/_d/ok/yf_dokzqy3vcritme8ggnzqlvwa.jpeg"
payload = {"body":
    {
    "url":hairy_potter
    }
}

payload = {"body":{
  'url': 'https://img.wattpad.com/da171ffe58dbf5469ce46124f5582d3167e3db26/68747470733a2f2f73332e616d617a6f6e6177732e636f6d2f776174747061642d6d656469612d736572766963652f53746f7279496d6167652f4a6b4d726d526b41536f6a6d68513d3d2d34342e313664373065353361623135343564323338343234303232343334342e6a7067?s=fit&w=720&h=720'
}}

r = requests.post(url, json=payload, timeout=30)

print(json.loads(r.text))

from time import sleep

import requests
import threading

url = "https://github.com/BinaryBreaker"
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

for i in range(100):
    a = requests.get(url, headers=headers)
    print(a.status_code)
    sleep(1/2)

import requests
import random
import json
from hashlib import md5

# 可以更换为你自己的appid/appkey.
appid = '20230805001770257'
appkey = '10MxfKpV0a5qT9s6fXt1'

# 如果需要更多语言的互译，请阅读以下地址 `https://api.fanyi.baidu.com/doc/21， 获取更多信息。`
from_lang = 'zh'
to_lang =  'en'

endpoint = 'http://api.fanyi.baidu.com'
path = '/api/trans/vip/translate'
url = endpoint + path

# Generate salt and sign
def make_md5(s, encoding='utf-8'):
    return md5(s.encode(encoding)).hexdigest()


def translate(query):
    salt = random.randint(32768, 65536)
    sign = make_md5(appid + query + str(salt) + appkey)

    # Build request
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    payload = {'appid': appid, 'q': query, 'from': from_lang, 'to': to_lang, 'salt': salt, 'sign': sign}

    # Send request
    r = requests.post(url, params=payload, headers=headers)
    result = r.json()

    results = json.dumps(result, indent=4, ensure_ascii=False)

    data = json.loads(results)

    # 获取目标值
    dst_value = data["trans_result"][0]["dst"]

    # 打印目标值
    # print(dst_value)

    return dst_value
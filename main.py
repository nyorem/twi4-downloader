#! /usr/bin/env python3

# Dependencies: requests
# TODO: switch to urllib

import os
import requests
import requests.packages.urllib3.util.connection as urllib3_cn
import urllib.request
import shutil

# force IPv4 in requests
# https://stackoverflow.com/questions/33046733/force-requests-to-use-ipv4-ipv6/46972341
def allowed_gai_family():
    import socket
    family = socket.AF_INET
    # if urllib3_cn.HAS_IPV6:
    #     family = socket.AF_INET6 # force ipv6 only if it is available
    return family
urllib3_cn.allowed_gai_family = allowed_gai_family

def pad_index(idx, n=4):
    idx_str = str(idx)
    zeros = n - len(idx_str)
    return "0" * zeros + idx_str

# 1. Download JS
comic = "fushigineko"
# comic = "kanako"
js_url = "https://sai-zen-sen.jp/comics/twi4/{}/index.js".format(comic)
r = requests.get(js_url)
assert r.status_code == 200

# https://stackoverflow.com/questions/44203397/python-requests-get-returns-improperly-decoded-text-instead-of-utf-8
r.encoding = r.apparent_encoding

# 2. Parse JS
contents = r.text
contents = contents[contents.find("Items")+8:-4]
contents = contents.split("{ ")[1:]

idx = 1
pages = []
for data in contents:
    data = data[:-4]
    data = data.split(", ")

    title = data[0].split(": ")[1][1:-1]
    suffix = data[-1].split(": ")[1][1:-1]

    idx_str = pad_index(idx)
    url = "https://sai-zen-sen.jp/comics/twi4/{}/works/{}{}.jpg".format(comic, idx_str, suffix)

    page = {
        "idx"  : idx_str,
        "title": title,
        "url"  : url,
    }

    idx += 1
    pages.append(page)

# TODO: cache pages

# 3. Download images (range)
if not os.path.isdir(comic):
    os.mkdir(comic)

# TODO: range of pages
for page in pages[:10]:
    print(page["idx"])

    fname = os.path.join(comic, page["idx"] + ".jpg")
    r = requests.get(page["url"])
    assert r.status_code == 200

    # https://stackoverflow.com/questions/13137817/how-to-download-image-using-requests
    with open(fname, "wb") as f:
        for chunk in r:
            f.write(chunk)

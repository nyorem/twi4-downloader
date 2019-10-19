import os
import requests

CACHE_DIR = "cache" # TODO: cache page list

# force IPv4 in requests
# https://stackoverflow.com/questions/33046733/force-requests-to-use-ipv4-ipv6/46972341
import requests.packages.urllib3.util.connection as urllib3_cn
def allowed_gai_family():
    import socket
    family = socket.AF_INET
    # if urllib3_cn.HAS_IPV6:
    #     family = socket.AF_INET6 # force ipv6 only if it is available
    return family
urllib3_cn.allowed_gai_family = allowed_gai_family

# Add zeros to a number such that the total length is equal to 'n'.
def pad_index(idx, n=4):
    idx_str = str(idx)
    zeros = n - len(idx_str)
    return "0" * zeros + idx_str

# Get the javascript file corresponding to the given comic.
# This file contains all the links to the images for each chapter.
def get_javascript(comic):
    js_url = "https://sai-zen-sen.jp/comics/twi4/{}/index.js".format(comic)
    r = requests.get(js_url)
    assert r.status_code == 200
    # https://stackoverflow.com/questions/44203397/python-requests-get-returns-improperly-decoded-text-instead-of-utf-8
    r.encoding = r.apparent_encoding
    return r.text

# Parse the javascript file as a list of pages, for each page, we have:
# - its number as a padded string
# - its title
# - the url of the corresponding image
def parse_javascript(comic, contents):
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

    return pages

def download_chapters(output_dir, pages, start=0, end=None, verbose=False):
    assert os.path.isdir(output_dir)

    for page in pages[start:end]:
        fname = page["idx"] + "-" + page["title"] + ".jpg"
        fname = os.path.join(output_dir, fname)
        if os.path.isfile(fname):
            if verbose:
                print("{} already downloaded, skipping...".format(fname))
            continue

        if verbose:
            print("Downloading {}".format(fname))

        r = requests.get(page["url"])
        if r.status_code != 200:
            if verbose:
                print("Chapter {} is not available".format(page["idx"]))
            continue

        # https://stackoverflow.com/questions/13137817/how-to-download-image-using-requests
        with open(fname, "wb") as f:
            for chunk in r:
                f.write(chunk)

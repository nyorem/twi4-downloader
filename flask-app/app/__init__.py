from flask import Flask, render_template, abort, jsonify

# Load comics informations once
import pickle
import os
COMICS = {}
COMICS_DIR = "../comics"
for fname in os.listdir(COMICS_DIR):
    if "pkl" not in fname:
        continue

    with open(os.path.join(COMICS_DIR, fname), "rb") as f:
        k = os.path.splitext(fname)[0]
        COMICS[k] = pickle.load(f)
        COMICS[k] = COMICS[k][:-1] # TODO: last chapter seems to be unavailable

app = Flask(__name__)

# Add zeros to a number such that the total length is equal to 'n'.
def pad_index(idx, n=4):
    idx_str = str(idx)
    zeros = n - len(idx_str)
    return "0" * zeros + idx_str

@app.route("/")
def index():
    comics_simple = []
    for k in COMICS.keys():
        comics_simple.append({
            "title": k,
            "last": "/{}/{}".format(k, COMICS[k][-1]["idx"]),
        })

    return render_template("index.html",
                           comics=comics_simple)

# Chapter as a route.
@app.route("/<string:comic>/<string:page>/")
def chapter(comic, page):
    if comic not in COMICS.keys():
        abort(404)

    pages = COMICS[comic]
    npages = len(pages)

    for p in pages:
        if p["idx"] == page:
            idx   = int(p["idx"])
            title = p["title"]
            url   = p["url"]

            next_idx     = "/{}/{}/".format(comic, pad_index(idx + 1)) if idx < npages else None
            previous_idx = "/{}/{}/".format(comic, pad_index(idx - 1)) if idx > 1 else None

            return render_template("chapter.html",
                                   comic=comic,
                                   title=title,
                                   url=url,
                                   current_chapter=idx,
                                   total_chapters=npages,
                                   next_chapter=next_idx,
                                   previous_chapter=previous_idx)

    abort(404)

# Chapter as a REST endpoint.
@app.route("/api/<string:comic>/<string:page>/")
def chapter_api(comic, page):
    if comic not in COMICS.keys():
        return jsonify({
            "success": False,
        }), 400

    pages  = COMICS[comic]
    npages = len(pages)

    for p in pages:
        if p["idx"] == page:
            idx   = int(p["idx"])
            title = p["title"]
            url   = p["url"]

            next_idx     = "/api/{}/{}/".format(comic, pad_index(idx + 1)) if idx < npages else None
            previous_idx = "/api/{}/{}/".format(comic, pad_index(idx - 1)) if idx > 1 else None

            return jsonify({
                "comic"          : comic,
                "current"        : p["idx"],
                "current_number" : idx,
                "title"          : title,
                "url"            : url,
                "next"           : next_idx,
                "previous"       : previous_idx,
            }), 200

    return jsonify({
        "success": False,
    }), 400

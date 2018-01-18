#!/usr/bin/env python3

from flask import Flask, render_template, send_from_directory, safe_join, jsonify, request
from flaskrun import flaskrun
import os

try:
    from natsort import natsorted as sort
except ImportError:
    sort = sorted

app = Flask(__name__)

@app.route("/")
def index():
    return send_from_directory(os.getcwd(), "index.html")

@app.route("/api1/")
def root():
    return jsonify(
        {
            "files": sort(f for f in os.listdir(".")
                          if not os.path.isdir(f)),
        })

@app.route("/api1/<filename>", methods=['GET', 'DELETE'])
def serve_file(filename):
    def get_file():
        return send_from_directory(os.getcwd(), filename)
    def delete_file():
        os.unlink(filename)
        return jsonify({'result': 'ok'})

    return {
        'GET': get_file,
        'DELETE': delete_file,
    }[request.method]()

if __name__ == '__main__':
    flaskrun(app, threaded=True)

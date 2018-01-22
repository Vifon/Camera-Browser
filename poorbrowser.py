#!/usr/bin/env python3

from flask import Flask, render_template, send_from_directory, safe_join, jsonify, request
from flask.ext.api import status
import os

try:
    from natsort import natsorted as sort
except ImportError:
    sort = sorted

app = Flask(__name__)

@app.route("/")
def index():
    return send_from_directory(os.getcwd(), "index.html")

@app.route("/v1/")
def list_files():
    return jsonify(
        {
            "files": sort(f for f in os.listdir(".")
                          if not os.path.isdir(f)),
        })

@app.route("/v1/<filename>", methods=['GET', 'DELETE', 'PUT'])
def serve_file(filename):
    def get_file():
        return send_from_directory(os.getcwd(), filename)

    def store_file():
        created = not os.path.exists(filename)
        with open(filename, 'wb') as stored_image:
            stored_image.write(request.data)

        if created:
            return (
                jsonify({'created': filename}),
                status.HTTP_201_CREATED
            )
        else:
            return (
                jsonify({'overwritten': filename}),
            )

    def delete_file():
        try:
            os.unlink(filename)
        except FileNotFoundError:
            return (
                jsonify({
                    'error': {
                        'not_found': filename,
                    },
                }),
                status.HTTP_404_NOT_FOUND
            )
        else:
            return (
                jsonify({'deleted': filename}),
            )

    return {
        'GET': get_file,
        'PUT': store_file,
        'DELETE': delete_file,
    }[request.method]()

if __name__ == '__main__':
    from flaskrun import flaskrun
    flaskrun(app, threaded=True)

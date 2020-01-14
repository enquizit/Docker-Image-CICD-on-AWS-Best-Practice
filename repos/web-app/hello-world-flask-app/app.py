# -*- coding: utf-8 -*-

from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello world!"

if __name__ == "__main__":
    import sys

    if len(sys.argv) >= 2:
        port = int(sys.argv[1])
    else:
        port = 80
    app.run(host="0.0.0.0", port=port, debug=True)

#!/usr/bin/python3

from flask import Flask, request, send_from_directory
app = Flask(__name__, static_url_path='')

@app.route('/')
def root():
    return """<!DOCTYPE html>
<html>
<head>
    <title>Tetris</title>
    <style>
        body {
            background-color: #272821;
        }
        .text {
            color: #706C5A;
            font-family: Inconsolata, Courier, monospace;
            font-size: 20px;
        }
        #score {
            padding-left: 55%;
        }
        #output {
            float: left;
            padding-left: 20%;
        }
    </style>
</head>
<body>
    <div id="output" class="text"></div>
    <div id="score" class="text"></div>
    <script src=./js/tetris.js></script>
    <script type="text/javascript"></script>
</body>
</html>"""

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)

if __name__ == "__main__":
    app.run()


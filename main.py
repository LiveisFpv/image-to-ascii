from Image2ascii import Image2ascii
import flask
from flask import Flask, render_template_string

# Создаем простой веб-сервер с Flask
app = Flask(__name__)

@app.route('/')
def home():
    return flask.render_template("index.html",frames=Image2ascii("files/02.gif",600).gif_to_ascii_frames())
if __name__ == "__main__":
    app.run(debug=True)
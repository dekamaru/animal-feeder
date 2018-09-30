from flask import Flask
from core import load

app = Flask(__name__)
container = load(app)

if __name__ == '__main__':
    app.run(port=8080)

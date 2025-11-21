from flask import Flask
from pprint import pprint

app = Flask(__name__)


@app.route('/')
def index_view():
    # pprint(app.config)
    return 'Совсем скоро тут будет случайное мнение о фильме!'

if __name__ == '__main__':
    app.run()
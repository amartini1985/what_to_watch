# what_to_watch/opinions_app/wsgi.py
import os
from . import app
import settings

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
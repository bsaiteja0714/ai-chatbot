import os
from app import app  # Make sure 'app.py' is in the same folder as 'wsgi.py'

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

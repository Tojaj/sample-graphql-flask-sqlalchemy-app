#!/usr/bin/env python

from app import app

# DEBUG
import logging

logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)

if __name__ == "__main__":
    app.run(debug=True)

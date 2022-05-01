# !/usr/bin/env python3

import os
import json
import sqlalchemy
import datetime
import zipfile
import random
import sys

from flask import Flask, render_template, request, send_file
from sqlalchemy.sql import text
from configparser import ConfigParser
from io import BytesIO

app = Flask(__name__)
app.config['TESTING'] = True

DATABASE_URL = f"postgresql://something or other"
engine = sqlalchemy.create_engine(DATABASE_URL)


# Route to homepage
@app.route("/")
def render_index():
    return render_template('home.html', page_title="Home")


# Necessary to run app if app.py is executed as a script
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
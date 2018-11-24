
import json
import gc
import sys
import traceback

# Data manipulation
import pandas as pd
import numpy as np

from flask import Flask, render_template, request, url_for, redirect, session, flash, jsonify

from db_extension import mysql

from blueprints.login import login_blueprint
from blueprints.search import search_blueprint

app = Flask(__name__)

app.config['DEBUG'] = True

app.secret_key = '\x96jF\xe7\xde\xe9 ]\x12C\x88\xaf\xf7W\xd5\xfdf\x87\xb1\x88xq\xff\x0f\xa3\x82\xaf=\xf6\xbe\xcd\x90\xcd\x92\x8c\xf4i\xa7\x7f\x8c'

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'testtest'
app.config['MYSQL_DATABASE_DB'] = 'CDS_breast_cancer'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

app.register_blueprint(login_blueprint)
app.register_blueprint(search_blueprint)




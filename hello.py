from functools import wraps
import json
import gc
import sys
import traceback

from flask import Flask, render_template, request, url_for, redirect, session, flash, jsonify

import csv

app = Flask(__name__)

<<<<<<< HEAD
# comment to test git 
# test 2
=======
@app.errorhandler(400)
def four_hundred_err(e):
    return render_template('400.html', error=e)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')


@app.errorhandler(500)
def five_hundred_err(e):
    return render_template('500.html', error=e)

# @app.route('/')
# def main():
#     return render_template('main.html')
>>>>>>> origin/master

@app.route('/')
@app.route('/login')
def login():
    return render_template('login.html')

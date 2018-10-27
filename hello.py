from functools import wraps
import json
import gc
import sys
import traceback

from flask import Flask, render_template, request, url_for, redirect, session, flash, jsonify

user_dict = { 
  '1': {
    'username': 'ABC',
    'password': '123'
  },
  '2': {
    'username': 'DEF',
    'password': '456'
  }
}

app = Flask(__name__)

@app.errorhandler(400)
def four_hundred_err(e):
  return render_template('400.html', error=e)


@app.errorhandler(404)
def page_not_found(e):
  return render_template('404.html')


@app.errorhandler(500)
def five_hundred_err(e):
  return render_template('500.html', error=e)

@app.route('/')
def redir_to_login():
  return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
    username = request.form['username']
    password = request.form['password']

    for user, values in user_dict.items():
      if username == values['username']:
        if password == values['password']:
          return redirect(url_for('mainpage'))
        else:
          return render_template('login.html')

      return render_template('login.html')

  else:
    return render_template('login.html')

@app.route('/main')
def mainpage():
  return render_template('main.html')
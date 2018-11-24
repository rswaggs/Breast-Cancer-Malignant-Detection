from flask import Blueprint, render_template, request, url_for, redirect, session, flash

from db_extension import mysql

# from blueprints.search import search_blueprint

login_blueprint = Blueprint("login", __name__)

@login_blueprint.route('/')
def redir_to_login():
  return redirect(url_for('login.login'))

@login_blueprint.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
    conn = mysql.connect()
    cursor = conn.cursor()

    cursor.callproc('GetUserData')
    user_data = cursor.fetchall()

    cursor.close()
    conn.close()

    username = request.form['username']
    password = request.form['password']
    
    for users in user_data:
      if username == users[3]:
        if password == users[4]:
          session['logged_in'] = True
          session['username'] = username
          return redirect(url_for('search.searchpage'))

        else:
          return render_template('views/login.html')

      return render_template('views/login.html')

  else:
    return render_template('views/login.html')
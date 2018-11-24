from functools import wraps
from flask import url_for, redirect, session

def login_req(f):
  @wraps(f)
  def wrap(*args, **kwargs):
    if 'logged_in' in session:
      return f(*args, **kwargs)

    else:
      return redirect(url_for('login.login'))

  return wrap

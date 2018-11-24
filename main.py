from functools import wraps
import json
import gc
import sys
import traceback

# Data manipulation
import pandas as pd
import numpy as np

# Libraries for model training and testing
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn import tree

# For storing model in memory
from sklearn.externals import joblib

from flask import Flask, render_template, request, url_for, redirect, session, flash, jsonify
from flaskext.mysql import MySQL

app = Flask(__name__)

app.config['DEBUG'] = True

app.secret_key = '\x96jF\xe7\xde\xe9 ]\x12C\x88\xaf\xf7W\xd5\xfdf\x87\xb1\x88xq\xff\x0f\xa3\x82\xaf=\xf6\xbe\xcd\x90\xcd\x92\x8c\xf4i\xa7\x7f\x8c'

# For local testing
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'testtest'
app.config['MYSQL_DATABASE_DB'] = 'CDS_breast_cancer'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

# Read in data
# Change to where dataset is saved
breast_cancer_df = pd.read_csv('./diagnosis_data.csv')

# Drop columns with not being used in model training/testing
breast_cancer_df = breast_cancer_df.drop(['id', 'radius_se', 'texture_se', 'perimeter_se', 'area_se', 
  'smoothness_se', 'compactness_se', 'smoothness_worst', 'compactness_worst', 'concavity_worst', 'concave points_worst',
  'concavity_se', 'concave points_se', 'symmetry_se',
  'fractal_dimension_se', 'radius_worst', 'texture_worst', 'perimeter_worst', 'area_worst', 
  'symmetry_worst', 'fractal_dimension_worst', 'Unnamed: 32'], axis=1)

# Predictor columns for X, truth labels for Y
X = breast_cancer_df.drop('diagnosis', axis=1)  
Y = breast_cancer_df['diagnosis']  

# Create train/test split
X_train, X_test, y_train, y_test = train_test_split( X, Y, test_size = 0.3, random_state = 100)

# Gini index for splitting
clf = DecisionTreeClassifier(criterion = "gini", random_state = 100,
                              max_depth=3, min_samples_leaf=5)

# Train
clf.fit(X_train, y_train)

# Save model in memory
joblib.dump(clf, 'model.pkl')

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


def login_req(f):
  @wraps(f)
  def wrap(*args, **kwargs):
    if 'logged_in' in session:
      return f(*args, **kwargs)

    else:
      return redirect(url_for('login'))

  return wrap


@app.route('/login', methods=['GET', 'POST'])
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
          return redirect(url_for('searchpage'))

        else:
          return render_template('login.html')

      return render_template('login.html')

  else:
    return render_template('login.html')

@app.route('/main')
def mainpage():
  return render_template('main.html', patients=patient_data)

@app.route('/search', methods=['GET', 'POST'])
@login_req
def searchpage():
  conn = mysql.connect()
  cursor = conn.cursor()

  cursor.callproc('GetPatientData')
  patient_data = cursor.fetchall()

  if request.method == "POST":

    patient = request.form['patient']

    patient_fname = str(patient).split()[0]
    patient_lname = str(patient).split()[1]

    cursor.callproc('GetOnePatient', (patient_fname, patient_lname))
    searched_patient_data = cursor.fetchall()[0]

    cursor.close()
    conn.close()

    if not searched_patient_data:
      return render_template('search.html', patient=None, patients=patient_data)

    else:
      return render_template('search.html', patient=searched_patient_data, patients=patient_data)
    
    return render_template('404.html')

  else:
    cursor.close()
    conn.close()
    return render_template('search.html', patient=None, patients=patient_data)

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

patient_data = {
'1': {
  'first_name': 'Balduin',
  'last_name': 'Rubinsaft',
  'age': 58,
  'gender': 'Male',
  'occupation': 'Geological Engineer',
  'last_appointment': '7/13/2018',
  'tumor_data_id': '842302'
},
'2': {
  'first_name': 'Carr',
  'last_name': 'Sancraft',
  'age': 49,
  'gender': 'Male',
  'occupation': 'Information Systems Manager',
  'last_appointment': '7/9/2018'
  },   
'3': {
  'first_name': 'Franchot',
  'last_name': 'MacKellar',
  'age': 61,
  'gender': 'Male',
  'occupation': 'Assistant Media Planner',
  'last_appointment': '11/5/2017'
},
'4': {
  'first_name': 'Vincenz',
  'last_name': 'Flieg',
  'age': 54,
  'gender': 'Male',
  'occupation': 'Dental Hygienist',
  'last_appointment': '1/17/2018'
}, 
'5': {
  'first_name': 'Phillip',
  'last_name': 'Brandon',
  'age': 56,
  'gender': 'Male',
  'occupation': 'Structural Engineer',
  'last_appointment': '11/15/2017'
}, 
'6': {
  'first_name': 'Ericha',
  'last_name': 'Rickaby',
  'age': 20,
  'gender': 'Female',
  'occupation': 'Dental Hygienist',
  'last_appointment': '4/23/2018'
}, 
'7': {
  'first_name': 'Emmye',
  'last_name': 'Handrick',
  'age': 27,
  'gender': 'Female',
  'occupation': 'Environmental Tech',
  'last_appointment': '7/21/2018'
}, 
'8': {
  'first_name': 'Dorothea',
  'last_name': 'Manston',
  'age': 32,
  'gender': 'Female',
  'occupation': 'Statistician IV',
  'last_appointment': '1/4/2018'
}, 
'9': {
  'first_name': 'Tasha',
  'last_name': 'Danks',
  'age': 39,
  'gender': 'Female',
  'occupation': 'Automation Specialist IV',
  'last_appointment': '11/22/2017'
}, 
'10' : {
  'first_name': 'Cliff',
  'last_name': 'Wrettum',
  'age': 33,
  'gender': 'Male',
  'occupation': 'Engineer III',
  'last_appointment': '8/17/2018'
  }
}

tumor_data = {
  '842302' : {
    'predicted_diagnosis' : 'N/A',
    'actual_diagnosis' : 'M',
    'radius_mean' : 17.99,
    'texture_mean' : 10.38,
    'perimeter_mean' : 122.8,
    'area_mean' : 1001,
    'smoothness_mean' : 0.1184, 
    'compactness_mean' : 0.2776,
    'concavity_mean' : 0.3001,
    'concave points_mean' : 0.1471,
    'symmetry_mean' : 0.2419,
    'fractal_dimension_mean' : 0.07871, 
    'radius_se' : 1.095,
    'texture_se' : 0.053,
    'perimeter_se' : 8.589,
    'area_se' : 153.4,
    'smoothness_se' : 0.006399,
    'compactness_se' : 0.04904,
    'concavity_se' : 0.05373,
    'concave points_se' : 0.01587,
    'symmetry_se' : 0.03003,
    'fractal_dimension_se' : 0.006193,
    'radius_worst' : 25.38,
    'texture_worst' : 17.33,
    'perimeter_worst' : 184.6,
    'area_worst' : 2019,
    'smoothness_worst' : 0.1622,
    'compactness_worst' : 0.6656,
    'concavity_worst' : 0.7119,
    'concave points_worst' : 0.2654,
    'symmetry_worst' : 0.4601,
    'fractal_dimension_worst' : 0.1189


  }
}
app = Flask(__name__)

app.config['DEBUG'] = True

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
  return render_template('main.html', patients=patient_data)

@app.route('/predict')
def predictpage():  
  return render_template('predict.html', tumor_data=tumor_data['842302'])

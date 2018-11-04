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

@app.route('/results')
def resultspage():
  
  	# Load model for prediction
    model = joblib.load('model.pkl')

    # OBTAIN DATA BY CSV FILE OR WEBFORM HERE
    patient_data_1 = [[20.57, 17.77, 132.9, 1326.0, 0.08474, 0.07864, 0.0869, 0.07017, 0.1812, 0.05667]]
    # patient_data_2 = [[17.99, 10.38, 122.8, 1001, 0.1184, 0.2776, 0.3001, 0.1471, 0.2419, 0.07871]]
    # patient_data_3 = [[13.54, 14.36, 87.46, 566.3, 0.09779, 0.08129, 0.06664, 0.04781, 0.1885, 0.05766]]

    # Play around with notebook to get familiar with how to extract the values
    # For value predicted
    result = model.predict(patient_data_1)

	  # For probabilities of certain classes being predicted
    model.predict_proba(patient_data_1)

    # Store features in JSON dictionary, or save in database before passing data to results page

    # Show results after prediction
    return render_template('results.html', result=result)
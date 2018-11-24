from flask import Blueprint, render_template, request, redirect, url_for, flash

# Database
from db_extension import mysql

# Handle data to run model
import csv
from ast import literal_eval   # String to dict, or list of dicts (for class_weights parameter)

# Data manipulation
import pandas as pd
import numpy as np

# Libraries for model training and testing
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn import tree

# For storing model in memory
import os
from sklearn.externals import joblib



# Create Blueprint
model_training_blueprint = Blueprint("model_training", __name__)



# Helper functions
'''
Description: Checks if string can be converted to a float.
Parameters: String object
Output: Boolean
'''
def isfloat(x):
    try:
        a = float(x)
    except ValueError:
        return False
    else:
        return True

'''
Description: Checks if string can be converted to a int.
Parameters: String object
Output: Boolean
'''
def isint(x):
    try:
        a = int(x)
    except ValueError:
        return False
    else:
        return True



'''
Author: Ryan Swaggert
Description: Returns the page to the user, in order to update models used for breast cancer predictions.
						The user will enter values for the decision tree classifier to be trained on.

Parameters: None
Output: HTML file. Goes to model page.
'''
@model_training_blueprint.route('/model')
def model():
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
        
		# SELECT * FROM model_update 
		# ORDER BY id
		# DESC LIMIT 1;
		cursor.callproc('GetLatestModelParameters')
		model_notes = cursor.fetchall()

		# Close database connection
		cursor.close() 
		conn.close()

		return render_template('views/model.html', model_notes=model_notes)
        
	except Exception as e:
		return render_template('error.html', error = str(e))


'''
Author: Ryan Swaggert
Description: The user enters values for the sklearn's decision tree classifier to be trained on.

Input: POST request of form inputs. Feature set(s) to run predictions on/
Output: Model file used to run predictions on gets updated. HTML file, goes to model page.
'''
@model_training_blueprint.route('/model_update', methods = ['POST'])
def model_update():
	try:
		if request.method == 'POST':
			
			# 1. Load in all the form values and change them to the appropriate type
			# 2. Load dataset from database
			# 3. Train model
			# 4. Save model


			# STEP 1
			# Load in all the form values and change them to the appropriate type
			# String
			criterion = request.form['criterion']

			# String
			splitter = request.form['splitter']

			# None, or int
			max_depth = request.form['max_depth']
			if max_depth == "None":
				max_depth = None
			else:
				max_depth = int(max_depth)

			# Float, or int
			min_samples_split = request.form['min_samples_split']
			if isint(min_samples_split):
				min_samples_split = int(min_samples_split)
			else:
				min_samples_split = float(min_samples_split)

			# Float, or int
			min_samples_leaf = request.form['min_samples_leaf']
			if isint(min_samples_leaf):
				min_samples_leaf = int(min_samples_leaf)
			else:
				min_samples_leaf = float(min_samples_leaf)

			# Float
			min_weight_fraction_leaf = request.form['min_weight_fraction_leaf']
			min_weight_fraction_leaf = float(min_weight_fraction_leaf)

			# None, float, int, or string
			max_features = request.form['max_features']
			if max_features == "None":
				max_features = None
			elif isint(max_features):
				max_features = int(max_features)
			elif isfloat(max_features):
				max_features = float(max_features)

			# None, or int (also suppose to accept RandomState instance)
			# Cannot accept for a string value RandomState instance a it is an object
			random_state = request.form['random_state']
			if random_state == "None":
				random_state = None
			else:
				random_state = int(random_state)

			# None, or int
			max_leaf_nodes = request.form['max_leaf_nodes']
			if max_leaf_nodes == "None":
				max_leaf_nodes = None
			else:
				max_leaf_nodes = int(max_leaf_nodes)

			# Float
			min_impurity_decrease = request.form['min_impurity_decrease']
			min_impurity_decrease = float(min_impurity_decrease)

			# None, dict, list of dicts, or "balanced"
			class_weight = request.form['class_weight']
			if class_weight == "None":
				class_weight = None
			elif class_weight == "Balanced":
				pass
			else:
				class_weight = literal_eval(class_weight)

			# Boolean
			presort = request.form['presort']
			if presort == "False":
				presort = False
			else:
				presort = True



			# STEP 2
			# Load dataset from database
			# Connect to database to download entries

			# Create directory to store temporary files
			if not os.path.exists("blueprints/temporary_files"):
				os.makedirs("blueprints/temporary_files")

			conn = mysql.connect()
			cursor = conn.cursor()
			
			'''SELECT diagnosis, 
				... ,
				fractal_dimension_mean 
			FROM train_data;'''
			cursor.callproc('GetTrainData')
			data = cursor.fetchall()

			with open("blueprints/temporary_files/breast_cancer.csv", "w") as dataset:
				fieldnames = ['diagnosis', 'radius_mean', 'texture_mean', 'perimeter_mean', 'area_mean',
					'smoothness_mean', 'compactness_mean', 'concavity_mean', 'concave points_mean', 
					'symmetry_mean', 'fractal_dimension_mean']
				writer = csv.DictWriter(dataset, fieldnames=fieldnames)

				# Create file
				writer.writeheader()
				for row in data:
					# First two rows are the id and upload_notes_id
					writer.writerow({'diagnosis': row[0], 'radius_mean': row[1], 'texture_mean': row[2], 
						'perimeter_mean': row[3], 'area_mean': row[4], 'smoothness_mean': row[5], 
						'compactness_mean': row[6], 'concavity_mean' : row[7], 'concave points_mean': row[8], 
						'symmetry_mean': row[9], 'fractal_dimension_mean': row[10]})


			# STEP 3
			# Train model
			breast_cancer_df = pd.read_csv("blueprints/temporary_files/breast_cancer.csv")
			
			# All values are used for training, since model with the above parameters is assumed to be tested
			X = breast_cancer_df.drop('diagnosis', axis=1)  
			Y = breast_cancer_df['diagnosis']

			# Gini index for splitting
			clf = DecisionTreeClassifier(criterion=criterion, splitter=splitter, max_depth=max_depth,
				min_samples_split=min_samples_split, min_samples_leaf=min_samples_leaf, 
				min_weight_fraction_leaf=min_weight_fraction_leaf, max_features=max_features,
				random_state=random_state, max_leaf_nodes=max_leaf_nodes, min_impurity_decrease=min_impurity_decrease,
				class_weight=class_weight, presort=presort)

			# Train
			clf.fit(X, Y)


			# STEP 4
			# Save model into file for later use
			joblib.dump(clf, 'blueprints/temporary_files/decision_tree_model.pkl')


			# STEP 5
			# Save parameters to database (we know model training went smoothly, without excepts)

			# Convert back to strings before running the query, as all values will be saved as strings
			#	in the database
			criterion = str(criterion)
			splitter = str(splitter)
			max_depth = str(max_depth)
			min_samples_split = str(min_samples_split)
			min_samples_leaf = str(min_samples_leaf)
			min_weight_fraction_leaf = str(min_weight_fraction_leaf)
			max_features = str(max_features)
			random_state = str(random_state)
			max_leaf_nodes = str(max_leaf_nodes)
			min_impurity_decrease = str(min_impurity_decrease)
			class_weight = str(class_weight)
			presort = str(presort)


			#for testing *(*Y*&T&843#@)
			_user = 32443


			'''INSERT INTO model_update
				(
					clinician_id,
  				update_time,
  				criterion,
  				... ,
  				presort
				)
				VALUES
				(
					entry_clinician_id,
  				NOW(),
  				entry_criterion,
  				... ,
  				entry_presort
				);'''
			cursor.callproc('AddToModelUpdates',(_user, criterion, splitter, max_depth, min_samples_split,
				min_samples_leaf, min_weight_fraction_leaf, max_features, random_state, max_leaf_nodes,
				min_impurity_decrease, class_weight, presort))

			# Save the insertion
			conn.commit()

			# Close database connection
			cursor.close() 
			conn.close()

			# Return to data route
			flash('Dataset successfully uploaded') 
			return redirect(url_for('model_training.model')) 

		else:
			return render_template('error.html') # Forces redirection to this url

	except Exception as e:
		return render_template('error.html',error = str(e))


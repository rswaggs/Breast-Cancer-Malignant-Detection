from flask import Blueprint, render_template, request, redirect, url_for, flash, Response, send_from_directory

# Handle file that holds multiple feature sets to be predicted
import csv
import io

# Import libraries to run predictions
from sklearn.externals import joblib
from sklearn.tree import DecisionTreeClassifier
from sklearn import tree

# Model plotting
from sklearn.tree import export_graphviz
from IPython.display import Image 
import pydotplus


# Create Blueprint
prediction_blueprint = Blueprint("prediction", __name__)



'''
Author: Ryan Swaggert
Description: Returns the page to the user where they can enter feature set(s)
						to get a breast cancer prediction for. Malignant/benign
Parameters: None
Output: HTML file
'''
@prediction_blueprint.route('/predict')
def predict_page():
	try:
		return render_template('views/predict.html')
        
	except Exception as e:
		flash(e)
		return render_template('error.html', error = str(e))


'''
Author: Ryan Swaggert
Description: Run the predictions, and then display the results of the /result route.
Input: POST request of feature set(s) to predict for.
Output: After successful prediction(s), redirect to /results to display results.
'''
@prediction_blueprint.route('/get_prediction', methods = ['POST'])
def predict():
	try:
		if request.method=='POST':
			
			# Load model for prediction
			model = joblib.load('blueprints/temporary_files/decision_tree_model.pkl')

			# Check if CSV of webform
			# Check if the post request has the file part
			if 'file' in request.files:
				file = request.files['file']

				# Deal with file inputs
				if file:
					stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
					reader = csv.DictReader(stream)

					# Store all the input sets to run predictions on
					input_data = []

					for row in reader:
						patient_id = int(row['patient_id'])
						radius_mean = float(row['radius_mean'])
						texture_mean = float(row['texture_mean'])
						perimeter_mean = float(row['perimeter_mean'])
						area_mean = float(row['area_mean'])
						smoothness_mean = float(row['smoothness_mean'])
						compactness_mean = float(row['compactness_mean'])
						concavity_mean = float(row['concavity_mean'])
						concave_points_mean = float(row['concave_points_mean'])
						symmetry_mean = float(row['symmetry_mean'])
						fractal_dimension_mean = float(row['fractal_dimension_mean'])

						one_input = [radius_mean, texture_mean, perimeter_mean, area_mean, smoothness_mean,
							compactness_mean, concavity_mean, concave_points_mean, symmetry_mean, fractal_dimension_mean]

						input_data.append(one_input)

				else:
					return render_template('error.html',error = str(e))
			
			# Else deal with webform inputs
			else:
				patient_id = int(row['patient_id'])
				radius_mean = float( request.form['radius_mean'] )
				texture_mean = float( request.form['texture_mean'] )
				perimeter_mean = float( request.form['perimeter_mean'] )
				area_mean = float( request.form['area_mean'] )
				smoothness_mean = float( request.form['smoothness_mean'] )
				compactness_mean = float( request.form['compactness_mean'] )
				concavity_mean = float( request.form['concavity_mean'] )
				concave_points_mean = float( request.form['concave_points_mean'] )
				symmetry_mean = float( request.form['symmetry_mean'] )
				fractal_dimension_mean = float( request.form['fractal_dimension_mean'] )

				# Input to prediction
				input_data = [[radius_mean, texture_mean, perimeter_mean, area_mean, smoothness_mean,
							compactness_mean, concavity_mean, concave_points_mean, symmetry_mean, fractal_dimension_mean]]


			# Now that we have the input array of predictions, the inputs can be run through prediction
			pred = model.predict(input_data)

			# The predicted class probability is the fraction of samples of the same class in a leaf.
			prob_pred = model.predict_proba(input_data)

			fi = model.feature_importances_


			# Iterate variables to limit decimal places before ending to template
			new_input_data = []
			for data_row in input_data:
				new_row = []
				for value in data_row:
					new_value = "{0:.2f}".format(value)
					new_row.append(new_value)
				new_input_data.append(new_row)

			new_prob_pred = []
			for data_row in prob_pred:
				new_row = []
				for value in data_row:
					new_value = "{0:.2f}".format(value)
					new_row.append(new_value)
				new_prob_pred.append(new_row)

			new_fi = []
			for value in fi:
				new_value = "{0:.3f}".format(value)
				new_fi.append(new_value)


			# Connect to database to store entries
			conn = mysql.connect()
			cursor = conn.cursor()

			# Enter the new predictions into the database
			for i in range(len(pred)):
				cursor.callproc('AddToPredictions',(patient_id, pred[i], new_prob_pred[0], new_prob_pred[1], 
				new_input_data[i][0], new_input_data[i][1], new_input_data[i][2], new_input_data[i][3], 
				new_input_data[i][4], new_input_data[i][5], new_input_data[i][6], new_input_data[i][7], 
				new_input_data[i][8], new_input_data[i][9]))

				# Save the row insertion
				conn.commit()

			# Close connection to database
			cursor.close() 
			conn.close()


			# Get the dot file data to turn into image
			dot_data = tree.export_graphviz(model, 
				out_file=None, 
				feature_names=['radius_mean', 'texture_mean', 'perimeter_mean', 'area_mean', 
					'smoothness_mean', 'compactness_mean', 'concavity_mean', 'concave points_mean', 
					'symmetry_mean', 'fractal_dimension_mean'],
				class_names=['Malignant', 'Benign'],
				filled=True, 
				rounded=True)

			# pydotplus is a Python Interface to Graphviz’s Dot language
			graph = pydotplus.graph_from_dot_data(dot_data)  

			# Show graph
			graph.write_png("blueprints/temporary_files/trained_tree.png")


			# Create dot file to download from
			with open("blueprints/temporary_files/decision_tree.dot", "w") as dot_file: 
				dot_file.write(dot_data) 


			# Pass prediction result to /result route and redirect
			return render_template('views/results.html', pred_results=pred, prob_pred_results=new_prob_pred, pred_inputs=new_input_data, feature_importances=new_fi)

	except Exception as e:
		return render_template('error.html',error = str(e))


'''
Author: Ryan Swaggert
Description: If the clinician needs a CSV template with the proper header format, 
            in order to run multiple predictions later they can download it by clicking
            the button to run this function. The downloaded CSV file only contains the 
            required headers, the clinician must add the required data to this CSV file 
            before further action.
Parameters: None
Output: Response object containing CSV file
'''
@prediction_blueprint.route('/prediction_csv_template')
def export_template_file():
	try:
		with open("prediction_template.csv", "w") as download_file:
			fieldnames = ['patient_id', 'pred_diagnosis', 'prob_classM', 'prob_classB', 'radius_mean', 
				'texture_mean', 'perimeter_mean', 'area_mean', 'smoothness_mean', 'compactness_mean', 
				'concave points_mean', 'symmetry_mean', 'fractal_dimension_mean']
			writer = csv.DictWriter(download_file, fieldnames=fieldnames)

			# Create file. Just require the header.
			writer.writeheader()

		# Download file
		return Response(download_file,
			mimetype="text/csv",
			headers={"Content-Disposition":
				"attachment;filename=prediction_cancer_template.csv"})

	except Exception as e:
		return render_template('error.html',error = str(e))

	else:
		''' Add send_from_directory maybe?
			I don't know if Response actually sends the file to the client,
			or it just creates the file for the server only.
		'''
		
		# Return to data route
		flash('Template file successfully downloaded')
		return redirect(url_for('data.data'))


'''
Author: Ryan Swaggert
Description: Get the train model image, and send it to the template to be displayed.
Input: GET request.
Output: Image location sent to /results HTML template.
'''
@prediction_blueprint.route('/trained_model_image')
def get_trained_model_image():
	try:
		return send_from_directory("blueprints/temporary_files", "trained_tree.png")
	except:
		return render_template('error.html',error = str(e))


'''
Author: Ryan Swaggert
Description: Get the dot file of the decision tree, for downloading.
Input: GET request.
Output: dot file from temporary files location.
'''
@prediction_blueprint.route('/decision_tree_dot_file')
def get_decision_tree_dot_file():
	try:
		return send_from_directory("blueprints/temporary_files", "decision_tree.dot")
	except:
		return render_template('error.html',error = str(e))


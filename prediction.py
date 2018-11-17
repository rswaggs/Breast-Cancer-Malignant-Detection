from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash, send_from_directory

# Handle file that holds multiple feature sets to be predicted
import csv

# Import libraries to run predictions
from sklearn.externals import joblib
from sklearn.tree import DecisionTreeClassifier
from sklearn import tree

# Model plotting
from sklearn.tree import export_graphviz
from IPython.display import Image 
import pydotplus


app = Flask(__name__)
app.secret_key = 'ESNlY88iNGA0iKh'


'''
Author: Ryan Swaggert
Description: Returns the page to the user where they can enter feature set(s)
						to get a breast cancer prediction for. Malignant/benign
Parameters: None
Output: HTML file
'''
@app.route('/')
@app.route('/predict')
def predict_page():
	try:
		return render_template('predict2.html')
        
	except Exception as e:
		flash(e)
		return render_template('404.html', error = str(e))


'''
Author: Ryan Swaggert
Description: Run the predictions, and then display the results of the /result route.
Input: POST request of feature set(s) to predict for.
Output: After successful prediction(s), redirect to /results to display results.
'''
@app.route('/get_prediction', methods = ['POST'])
def predict():
	try:
		if request.method=='POST':
			
			# Load model for prediction
			model = joblib.load('temporary_files/model.pkl')

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
					flash("Where did you go file?")
					return render_template('404.html',error = str(e))
			
			# Else deal with webform inputs
			else:
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
				input_data = [radius_mean, texture_mean, perimeter_mean, area_mean, smoothness_mean,
							compactness_mean, concavity_mean, concave_points_mean, symmetry_mean, fractal_dimension_mean]


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



			# Get the dot file data to turn into image
			dot_data = tree.export_graphviz(model, 
				out_file=None, 
				feature_names=['radius_mean', 'texture_mean', 'perimeter_mean', 'area_mean', 
					'smoothness_mean', 'compactness_mean', 'concavity_mean', 'concave points_mean', 
					'symmetry_mean', 'fractal_dimension_mean'],
				class_names=['Malignant (spreading)', 'Benign (not spreading)'],
				filled=True, 
				rounded=True)

			# pydotplus is a Python Interface to Graphviz’s Dot language
			graph = pydotplus.graph_from_dot_data(dot_data)  

			# Show graph
			graph.write_png("temporary_files/trained_tree.png")


			# Pass prediction result to /result route and redirect
			render_template('results2.html', pred_results=pred, prob_pred_results=new_prob_pred, pred_inputs=new_input_data, feature_importances=new_fi)

	except Exception as e:
		flash(e)
		return render_template('404.html',error = str(e))


'''
Author: Ryan Swaggert
Description: Get the train model image, and send it to the template to be displayed.
Input: GET request.
Output: Image location sent to /results HTML template.
'''
@app.route('/trained_model_image')
def get_trained_model_image():
    return send_from_directory("temporary_files", "trained_tree.png")


if __name__ == '__main__':
   app.run(debug = True)
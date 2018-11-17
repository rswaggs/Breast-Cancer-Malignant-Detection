from flask import Flask, Blueprint, render_template, request, redirect, url_for, Response, flash
from flaskext.mysql import MySQL

# Read CSV file
import csv, io

# Get time of data upload
import time


# Look up Blueprints before submitting code

#data_upload = Blueprint('data_upload', __name__)
app = Flask(__name__)
app.secret_key = 'ESNlY88iNGA0iKh'

# For local testing
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'CDS_breast_cancer'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)




# Helper function
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
Author: Ryan Swaggert
Description: Returns the page to the user, in order to upload / download data from the data table in 
            the database. The table that stores data is comprised of datasets used for model training.

						Upload notes about the dataset uploads are loaded from the database to display at the 
						bottom of the page.

Parameters: None
Output: HTML file
'''
# Data routes
#@data_upload.route('/data')
@app.route('/')
@app.route('/data')
def data():
  try:
		conn = mysql.connect()
		cursor = conn.cursor()
        
		cursor.callproc('GetUploadNotes')
		upload_notes = cursor.fetchall()

		# Close database connection
		cursor.close() 
		conn.close()

		return render_template('data.html', notes_data=upload_notes)
        
	except Exception as e:
		flash(e)
		return render_template('404.html', error = str(e))



'''
Author: Ryan Swaggert
Description: If the clinician obtains new datasets containing breast cancer features and their 
            outcomes, they can upload that dataset. The dataset will be saved to the data table
            in the database, and upload notes will be saved to the upload table.
Parameters: None
Output: None, redirects to /data
'''
#@data_upload.route('/data_upload', methods = ['GET', 'POST'])
@app.route('/data_upload', methods = ['POST'])
def data_upload():
	try:
		if request.method == 'POST':
			
			# Check if the post request has the file part
			if 'file' not in request.files:
				flash('No file part')
				return redirect(url_for('data'))
			file = request.files['file']

			if file:
				
				#for testing *(*Y*&T&843#@)
				_user = 32443
        		
				# Time database rows are started to be updated
				_current_time = time.strftime('%Y-%m-%d %H:%M:%S')

				# Store userform data into data_upload_notes table
				_updateNotes = request.form['inputNotes']


				# Connect to database to store entries
				conn = mysql.connect()
				cursor = conn.cursor()
				
				# Add to data_upload_notes table
				cursor.callproc('AddToUploadNotes',(_user,_current_time,_updateNotes))
				
				# Save the row insertion
				conn.commit()

				# Make call to data_upload_notes table to get current id for most recent entry
				# The foregin key will ensure CSV and upload tables can be joined to find time of
				#     upload for each table entry
				# Get last update notes ID inserted - Get the last ID auto-increment added to any table
				cursor.callproc('GetUploadNotesMostRecentID')
				update_notes_id = cursor.fetchone()

				# Read csv file to save into mySQL database
				stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
				reader = csv.DictReader(stream)
				 
        # Check that label exists for set of features, for each row
        # Check that all values are char/float, for each row
        # Limit the amount of decimal places to be able to store value in mySQL database
				for row in reader:
					if not row['diagnosis'].isalpha() or row['diagnosis'] == "":
						continue

					if isfloat(row['radius_mean']):
						v_radius_mean = float("{0:.5f}".format( float(row['radius_mean']) ))
					else:
						v_radius_mean = -1.0

					if isfloat(row['texture_mean']):
						v_texture_mean = float("{0:.5f}".format( float(row['texture_mean']) ))
					else:
						v_texture_mean = -1.0

					if isfloat(row['perimeter_mean']):
						v_perimeter_mean = float("{0:.5f}".format( float(row['perimeter_mean']) ))
					else:
						v_perimeter_mean = -1.0

					if isfloat(row['area_mean']):
						v_area_mean = float("{0:.5f}".format( float(row['area_mean']) ))
					else:
						v_area_mean = -1.0

					if isfloat(row['smoothness_mean']):
						v_smoothness_mean = float("{0:.5f}".format( float(row['smoothness_mean']) ))
					else:
						v_smoothness_mean = -1.0

					if isfloat(row['compactness_mean']):
						v_compactness_mean = float("{0:.5f}".format( float(row['compactness_mean']) ))
					else:
						v_compactness_mean = -1.0

					if isfloat(row['concavity_mean']):
						v_concavity_mean = float("{0:.5f}".format( float(row['concavity_mean']) ))
					else:
						v_concavity_mean = -1.0

					if isfloat(row['concave points_mean']):
						v_concave_points_mean = float("{0:.5f}".format( float(row['concave points_mean']) ))
					else:
						v_concave_points_mean = -1.0

					if isfloat(row['symmetry_mean']):
						v_symmetry_mean = float("{0:.5f}".format( float(row['symmetry_mean']) ))
					else:
						v_symmetry_mean = -1.0

					if isfloat(row['fractal_dimension_mean']):
						v_fractal_dimension_mean = float("{0:.5f}".format( float(row['fractal_dimension_mean']) ))
					else:
						v_fractal_dimension_mean = -1.0


					# Save the current row into the data database
					cursor.callproc('AddToTrainData',(update_notes_id, row['diagnosis'], v_radius_mean, 
						v_texture_mean, v_perimeter_mean, v_area_mean, v_smoothness_mean,
						v_compactness_mean, v_concavity_mean, v_concave_points_mean, 
						v_symmetry_mean, v_fractal_dimension_mean))

					# Save the row insertion
					conn.commit()
        
        # Close connection to database
				cursor.close() 
				conn.close() 


				# Return to data route
				flash('Dataset successfully uploaded') 
				return redirect(url_for('data')) 

		else:
			return render_template('404.html',error = str(e)) # Forces redirection to this url

	except Exception as e:
		flash(e)
		return render_template('404.html',error = str(e))


'''
Author: Ryan Swaggert
Description: If the clinician needs a CSV template with the proper header format, 
            in order to run predictions later or upload the data to the MySQL database, 
            they can download it by clicking the button to run this function. The 
            downloaded CSV file only contains the required headers, the clinician
            must add the required data to this CSV file before further action.
Parameters: None
Output: Response object containing CSV file
'''
@app.route('/data_csv_template')
def export_template_file():
	try:
		with open("breast_cancer_template.csv", "w") as download_file:
			fieldnames = ['diagnosis', 'radius_mean', 'texture_mean', 'perimeter_mean', 'area_mean',
				'smoothness_mean', 'compactness_mean', 'concave points_mean', 'symmetry_mean', 'fractal_dimension_mean']
			writer = csv.DictWriter(download_file, fieldnames=fieldnames)

			# Create file. Just require the header.
			writer.writeheader()

		# Download file
		return Response(download_file,
			mimetype="text/csv",
			headers={"Content-Disposition":
				"attachment;filename=breast_cancer_template.csv"})

	except Exception as e:
		flash(e)
		return render_template('404.html',error = str(e))

	else:
		# Return to data route
		flash('Template file successfully downloaded')
		return redirect(url_for('data'))


'''
Author: Ryan Swaggert
Description: For clinicians familiar with machine learning, they can download the current dataset
            stored in the MySQL database. The data in the MySQL database serves as a private health
            dataset for the users of the system. The dataset enables further improvement of the 
            accuracy of the prediction system, by allowing the authorized users to download the
            dataset to use to train new machine learning models for the system.
Parameters: None
Output: Response object containing CSV file
'''
@app.route('/data_download')
def export_file():
	try:
		# Connect to database to download entries
		conn = mysql.connect()
		cursor = conn.cursor()

		cursor.callproc('GetTrainData')
		data = cursor.fetchall()

		with open("breast_cancer.csv", "w") as download_file:
			fieldnames = ['diagnosis', 'radius_mean', 'texture_mean', 'perimeter_mean', 'area_mean',
				'smoothness_mean', 'compactness_mean', 'concavity_mean', 'concave points_mean', 
				'symmetry_mean', 'fractal_dimension_mean']
			writer = csv.DictWriter(download_file, fieldnames=fieldnames)

			# Create file
			writer.writeheader()
			for row in data:
				# First two rows are the id and upload_notes_id
				writer.writerow({'diagnosis': row[0], 'radius_mean': row[1], 'texture_mean': row[2], 
					'perimeter_mean': row[3], 'area_mean': row[4], 'smoothness_mean': row[5], 
					'compactness_mean': row[6], 'compactness_mean' : row[7], 'concave points_mean': row[8], 
					'symmetry_mean': row[9], 'fractal_dimension_mean': row[10]})

		# Close database connection
		cursor.close() 
		conn.close()

    # Download file
		return Response(download_file,
			mimetype="text/csv",
      headers={"Content-Disposition":
        "attachment;filename=breast_cancer.csv"})

	except Exception as e:
		flash(e)
		return render_template('404.html',error = str(e))

	else:
		# Return to data route
		flash('Dataset successfully downloaded')
		return redirect(url_for('data'))



if __name__ == '__main__':
   app.run(debug = True)
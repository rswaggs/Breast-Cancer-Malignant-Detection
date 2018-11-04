from flask import Flask, Blueprint, render_template, request, redirect, url_for, Response
from flaskext.mysql import MySQL
from werkzeug import secure_filename
import csv
import time

# Look up Blueprints before submitting code

#data_upload = Blueprint('data_upload', __name__)
app = Flask(__name__)

mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'CDS_breast_cancer'
app.config['MYSQL_DATABASE_HOST'] = '127.0.0.1'
mysql.init_app(app)

''' Example using flask.ext.mysql
conn = mysql.connect()
cursor = conn.cursor()

cursor.execute("SELECT * from User")
data = cursor.fetchone()'''



# Data routes
#@data_upload.route('/data')
@app.route('/')
@app.route('/data')
def data():
  return render_template('data.html')

'''# Get data to display for data route
@app.route('/getData')
def getData():
	try:
        conn = mysql.connect()
        cursor = conn.cursor()
        
        cursor.callproc('GetUploadNotes')
        upload_notes = cursor.fetchall()

        notes_dict = []
        for note in upload_notes:
            note_dict = {
                    'ID': note[0],
                    'Clinician ID': note[1],
                    'Upload time': note[2],
                    'Source note': blog[3]}
            notes_dict.append(note_dict)

        return json.dumps(notes_dict)
        
    except Exception as e:
		return render_template('error.html', error = str(e))'''


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
@app.route('/data_csv_template', methods = ['GET', 'POST'])
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
    return render_template('404.html',error = str(e))
  finally:
    # Return to data route
    return redirect(url_for('data'))


'''
#@data_upload.route('/data_upload', methods = ['GET', 'POST'])
@app.route('/data_upload', methods = ['GET', 'POST'])
def data_upload():
	try:
		if request.method == 'POST':

        	# check if the post request has the file part
        	if 'file' not in request.files:
            	flash('No file part')
            	return redirect(url_for('data'))
        	file = request.files['file']

        	# if user does not select file, browser also
        	# submit a empty part without filename
        	if file.filename == '':
            	flash('No selected file')
            	return redirect(url_for('data'))

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
            	data = cursor.fetchall()

            	# Commit to database if query is successful
            	if len(data) is 0:
    				conn.commit()
    			else:
    				return render_template('error.html',error = 'An error occurred!')


    			# Get last update notes ID inserted
            	cursor.callproc('GetUploadNotesMostRecentID')
            	update_notes_id = cursor.fetchone()


            	reader = csv.DictReader(file)

            	# Make call to data_upload_notes table to get current id for most recent entry
            	# The foregin key will ensure CSV and upload tables can be joined to find time of
            	#     upload for each table entry
            
            	for row in reader:
            		# Check that all values are char/float first
            		# Set to value for later if so, or continue to next entry if no label exists
            		if not row['diagnosis'].isalpha() or row['diagnosis'] == "":
            			continue
            		if not isinstance(row['radius_mean'], float):
            			row['radius_mean'] = -1.0
            		if not isinstance(row['texture_mean'], float):
            			row['radius_mean'] = -1.0
            		if not isinstance(row['perimeter_mean'], float):
            			row['radius_mean'] = -1.0
            		if not isinstance(row['area_mean'], float):
            			row['radius_mean'] = -1.0
            		if not isinstance(row['smoothness_mean'], float):
            			row['radius_mean'] = -1.0
            		if not isinstance(row['compactness_mean'], float):
            			row['radius_mean'] = -1.0
            		if not isinstance(row['concavity_mean'], float):
            			row['radius_mean'] = -1.0
            		if not isinstance(row['concave points_mean'], float):
            			row['radius_mean'] = -1.0
            		if not isinstance(row['symmetry_mean'], float):
            			row['radius_mean'] = -1.0
            		if not isinstance(row['fractal_dimension_mean'], float):
            			row['radius_mean'] = -1.0

            		cursor.callproc('AddToTrainData',(update_notes_id["id"], row['diagnosis'], row['radius_mean'], row['texture_mean'],
            			row['perimeter_mean'], row['area_mean'], row['smoothness_mean'], row['compactness_mean'],
            			row['concave points_mean'], row['symmetry_mean'], row['fractal_dimension_mean']))
        
        else:
        	return render_template('error.html',error = str(e)) # Forces redirection to this url
    except Exception as e:
        return render_template('error.html',error = str(e))
    finally:
        cursor.close() 
        conn.close()   

        # Return to data route
        return redirect(url_for('data'))     
''' 


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
@app.route('/data_download', methods=['GET', 'POST'])
def export_file():
	try:
		if request.method == 'POST':

			# Connect to database to download entries
      conn = mysql.connect()
      cursor = conn.cursor()

      cursor.callproc('GetTrainData')
      data = cursor.fetchall()

      with open("breast_cancer.csv", "w") as download_file:
        fieldnames = ['diagnosis', 'radius_mean', 'texture_mean', 'perimeter_mean', 'area_mean',
          'smoothness_mean', 'compactness_mean', 'concave points_mean', 'symmetry_mean', 'fractal_dimension_mean']
        writer = csv.DictWriter(download_file, fieldnames=fieldnames)

        # Create file
        writer.writeheader()
        for row in data:
          # First two row indices are user and datetime
          writer.writerow({'diagnosis': row[0], 'radius_mean': row[1], 'texture_mean': row[2], 
            'perimeter_mean': row[3], 'area_mean': row[4], 'smoothness_mean': row[5], 
            'compactness_mean': row[6], 'concave points_mean': row[7], 'symmetry_mean': row[8], 
            'fractal_dimension_mean': row[9]})

      # Download file
      return Response(writer,
        mimetype="text/csv",
        headers={"Content-Disposition":
          "attachment;filename=breast_cancer.csv"})

  except Exception as e:
    return render_template('404.html',error = str(e))
  finally:
    cursor.close() 
    conn.close()   

    # Return to data route
    return redirect(url_for('data'))



if __name__ == '__main__':
   app.run(debug = True)
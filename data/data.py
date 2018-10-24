from flask import Flask, Blueprint, render_template, request, redirect, url_for
from flask.ext.mysql import MySQL
from werkzeug import secure_filename
import csv

# Uncomment Blueprint stuff before production

#data_upload = Blueprint('data_upload', __name__)
app = Flask(__name__)

mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'CDS_breast_cancer'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

ALLOWED_EXTENSIONS = set(['csv'])

# Supporting functions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Data routes
#@data_upload.route('/data')
@app.route('/data')
def data():
	return render_template('data.html')


#@data_upload.route('/data_upload', methods = ['GET', 'POST'])
@app.route('/data_upload', methods = ['GET', 'POST'])
def data():
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

        if file and allowed_file(file.filename):
            reader = csv.DictReader(file)
            
            for row in reader:
            	row['diagnosis']

            	row['radius_mean']
            	row['texture_mean']
            	row['perimeter_mean']
            	row['area_mean']
            	row['smoothness_mean']
            	row['compactness_mean']
            	row['concavity_mean']
            	row['concave points_mean']
            	row['symmetry_mean']
            	row['fractal_dimension_mean']

            	row['radius_se']
            	row['texture_se']
            	row['perimeter_se']
            	row['area_se']
            	row['smoothness_se']
            	row['compactness_se']
            	row['concavity_se']
            	row['concave points_se']
            	row['symmetry_se']
            	row['fractal_dimension_se']

            	row['radius_worst']
            	row['texture_worst']
            	row['perimeter_worst']
            	row['area_worst']
            	row['smoothness_worst']
            	row['compactness_worst']
            	row['concavity_worst']
            	row['concave points_worst']
            	row['symmetry_worst']
            	row['fractal_dimension_worst']

        	for row in data:
            	date_time_store = row['date_time']
            technician_store = row['technician']
            test_location_store = row['test_location']
            product_serial_number_store = row['product_serial_number']
            test_detail_store = row['test_detail']
            test_result_store = row['test_result']
 
            query = test_result(date_time = date_time_store,
                                technician_name = technician_store,
                                place_of_test = test_location_store,
                                serial_number=product_serial_number_store,
                                test_details=test_detail_store,
                                result=test_result_store)
 
 			# validate the received values
        	if _name and _email and _password:
            
            	# All Good, let's call MySQL
            
            	conn = mysql.connect()
            	cursor = conn.cursor()

            db.session.add(query)
        db.session.commit()
        return('Did it work?')
    else:
        return redirect(url_for('upload_csv.upload_csv_layout'))# Forces redirection to this url


if __name__ == '__main__':
   app.run(debug = True)
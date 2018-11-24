from flask import Flask, render_template

# Database
from db_extension import mysql

# Blueprints registering
from blueprints.data import data_blueprint
from blueprints.model import model_training_blueprint
from blueprints.prediction import prediction_blueprint

# Host the application here
from blueprints.login import login_blueprint
from blueprints.search import search_blueprint

app = Flask(__name__)
app.secret_key = 'ESNlY88iNGA0iKh'

# Database
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'CDS_breast_cancer'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

mysql.init_app(app)

# Drop columns with not being used in model training/testing
breast_cancer_df = breast_cancer_df.drop(['id', 'radius_se', 'texture_se', 'perimeter_se', 'area_se', 
  'smoothness_se', 'compactness_se', 'smoothness_worst', 'compactness_worst', 'concavity_worst', 'concave points_worst',
  'concavity_se', 'concave points_se', 'symmetry_se',
  'fractal_dimension_se', 'radius_worst', 'texture_worst', 'perimeter_worst', 'area_worst', 
  'symmetry_worst', 'fractal_dimension_worst', 'Unnamed: 32'], axis=1)

app.register_blueprint(login_blueprint)
app.register_blueprint(search_blueprint)
# Register blueprints
app.register_blueprint(data_blueprint)
app.register_blueprint(model_training_blueprint)
app.register_blueprint(prediction_blueprint)

'''
APPLICATION
'''
@app.route('/')
@app.route('/main')
def main_page():
	try:
		return render_template('main.html')
        
	except Exception as e:
		return render_template('error.html', error = str(e))


'''
RUN
'''
if __name__ == "__main__":
	app.run(debug=True)
from flask import Flask, render_template

# Database
from db_extension import mysql

# Blueprints registering
from blueprints.data import data_blueprint
from blueprints.model import model_training_blueprint
from blueprints.prediction import prediction_blueprint
from blueprints.login import login_blueprint
from blueprints.search import search_blueprint

from wrapper_funcs import login_req

app = Flask(__name__)
app.secret_key = 'ESNlY88iNGA0iKh'

# Database
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''  
app.config['MYSQL_DATABASE_DB'] = 'cds_breast_cancer'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'


mysql.init_app(app)

# Register blueprints
app.register_blueprint(login_blueprint)
app.register_blueprint(search_blueprint)
app.register_blueprint(data_blueprint)
app.register_blueprint(model_training_blueprint)
app.register_blueprint(prediction_blueprint)

'''
APPLICATION
'''
@app.route('/main')
@login_req
def main_page():
	try:
		return render_template('main.html')

	except Exception as e:
		return render_template('error.html', error = str(e))


'''
RUN
'''
if __name__ == "__main__":
	app.run()

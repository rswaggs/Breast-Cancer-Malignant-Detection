from flask import Flask, Blueprint, render_template, request, redirect, url_for, Response

# Data manipulation
import pandas as pd
import numpy as np

# Libraries for model training and testing
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn import tree

# For storing model in memory
from sklearn.externals import joblib

app = Flask(__name__)


#Look up next:
#https://blog.hyperiondev.com/index.php/2018/02/01/deploy-machine-learning-model-flask-api/

#https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=2&cad=rja&uact=8&ved=2ahUKEwibpbavo6reAhUurlkKHUBBDVcQFjABegQICBAB&url=https%3A%2F%2Fwww.wintellect.com%2Fcreating-machine-learning-web-api-flask%2F&usg=AOvVaw2JaswVXFpHGWJSta8ODdBc
#https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=1&cad=rja&uact=8&ved=2ahUKEwibpbavo6reAhUurlkKHUBBDVcQFjAAegQIBRAB&url=https%3A%2F%2Fwww.toptal.com%2Fpython%2Fpython-machine-learning-flask-example&usg=AOvVaw3pUXyhdMlXZ-a4k1qBM-Pn
#https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=14&cad=rja&uact=8&ved=2ahUKEwibpbavo6reAhUurlkKHUBBDVcQFjANegQIAxAB&url=https%3A%2F%2Fwww.analyticsvidhya.com%2Fblog%2F2017%2F09%2Fmachine-learning-models-as-apis-using-flask%2F&usg=AOvVaw3o3b-YLsWISwDGSBC2xNU4


#https://medium.com/@dvelsner/deploying-a-simple-machine-learning-model-in-a-modern-web-application-flask-angular-docker-a657db075280
# Now the training can be triggered by calling the 
# endpoint http://localhost:8081/api/train with a HTTP POST request.




@app.route('/api/predict', methods=['POST'])
def predict():
    # get iris object from request
    X = request.get_json()
    X = [[float(X['sepalLength']), float(X['sepalWidth']), float(X['petalLength']), float(X['petalWidth'])]]

    # read model
    clf = joblib.load('model.pkl')
    probabilities = clf.predict_proba(X)

    return jsonify([{'name': 'Iris-Setosa', 'value': round(probabilities[0, 0] * 100, 2)},
                    {'name': 'Iris-Versicolour', 'value': round(probabilities[0, 1] * 100, 2)},
                    {'name': 'Iris-Virginica', 'value': round(probabilities[0, 2] * 100, 2)}])




@app.route('/predict', methods=['POST'])
def predict():
  if request.method=='POST':

  	# Load model for prediction
    model = joblib.load('model.pkl')

    # OBTAIN DATA BY CSV FILE OR WEBFORM HERE
    # patient_data = [[20.57, 17.77, 132.9, 1326.0, 0.08474, 0.07864, 0.0869, 0.07017, 0.1812, 0.05667]]

    # Play around with notebook to get familiar with how to extract the values
    # For value predicted
    model.predict(patient_data)
	# For probabilities of certain classes being predicted
    model.predict_proba(patient_data)

    # Store features in JSON dictionary, or save in database before passing data to results page

    # Show results after prediction
    return render_template('results.html')



    # GREAT CODE TO FOLLOW IF YOU WANT TO PASS THE CODE THROUGH JSON
    # Grab features to predict for
    feature_array = request.get_json()['feature_array']
    
    #our model rates the wine based on the input array
    prediction = model.predict([feature_array]).tolist()
    
    #preparing a response object and storing the model's predictions
    response = {}
    response['predictions'] = prediction
    
    #sending our response object back as json
    # May help bind to the HTML sending the response as JSON
    return flask.jsonify(response)


if __name__ == '__main__':

  # Read in data
  # Change to where dataset is saved
  breast_cancer_df = pd.read_csv('../diagnosis_data.csv')

  # Drop columns with not being used in model training/testing
  breast_cancer_df = breast_cancer_df.drop(['id', 'radius_se', 'texture_se', 'perimeter_se', 'area_se', 
    'smoothness_se', 'compactness_se', 'concavity_se', 'concave points_se', 'symmetry_se',
    'fractal_dimension_se', 'radius_worst', 'texture_worst', 'perimeter_worst', 'area_worst', 
    'smoothness_worst', 'compactness_worst', 'concavity_worst', 'concave points_worst',
    'symmetry_worst', 'fractal_dimension_worst', 'Unnamed: 32'], axis=1)

  # Predictor columns for X, truth labels for Y
  X = breast_cancer_df.drop('diagnosis', axis=1)  
  y = breast_cancer_df['diagnosis']  

  # Create train/test split
  X_train, X_test, y_train, y_test = train_test_split( X, Y, test_size = 0.3, random_state = 100)

  # Gini index for splitting
  clf = DecisionTreeClassifier(criterion = "gini", random_state = 100,
                               max_depth=3, min_samples_leaf=5)

  # Train
  clf.fit(X_train, y_train)

  # Save model in memory
  joblib.dump(clf, 'model.pkl')


  # START APP
  app.run(debug = True)





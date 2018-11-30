# Breast-Cancer-Malignant-Detection

As part of our clincial decision support course (computer science), we were tasked with creating a system to assist healthcare professionals. For our system, we used [UCI Irvine Machine Learning Repository’s Breast Cancer Wisconsin (Diagnostic) dataset](http://archive.ics.uci.edu/ml/datasets/Breast+Cancer) to classify if patients have malignant or benign cancer.

Since the goal was decision support, the goal of the project was to develop a machine learning model that clinicians could use to assist them in their decision process. It was not met as a way to give a final answer as to whether patients had malignant cancer.

Features:
- The main feature is the decision tree classifier to classify the breast cancer features as malignant or benign.
- Login (assuming a database adminstator would add clinicians, elimiting the need for a signup feature).
- Patient search. To find and analyze a single patient's data.
- Database downloading/uploading of datasets. Using CSV files, new datasets could be concatenated to the exist dataset stored in the database. The data in the database could also be downloaded for further use.
- Model updating. Using the sklearn DecisionTreeClassifier as a guide, the user could update the model that the decision support system uses, by entering the appropriate values in the web form and submitting.
- Prediction and results. For new feature set(s), the prediction results and plot of the current model is displayed to the user. The plot assists the clinician in their final decision.

Development tools:
- Frontend. HTML5, CSS3, Bootstrap.
- Backend. Flask, MySQL (stored procedures).
- Machine learning. sklearn.


# Instructions for TA to test
#### It's important to follow the guide in order, as the model needs data in the database to be trained, and the prediction page needs a model to run a prediction.
##### The main.py code connects all the separate Python files to work together using blueprints.
1. Enter website
  - http://165.227.38.228:5000/login
2. Test login (code in views/login.html, blueprints/login.py, wrapper_funcs.py)
  - Try navigating to /model, /data, /main, etc without logging in first
  - Try testing random incrrect username and passcode
3. Search page (views/search.html, blueprints/search.py)
  - Note: We were planning to make this work so that the user could look up the tumor prediction results to quickly view those results from this page. But, there did not end up being enough time.
  - For testing, start typing any cahracters. Names will show up that match the character patterns. You can use patient details once a name is selected.
3. Data button (code in views/data.html and blueprints/data.py)
  - Push get template and get dataset buttons
	  - Template should be CSV file with just headers
	  - If there is data in the database, get dataset should have the headers and data rows stored as many entries in the database
  - Now try to upload data
	  - If there is no data in the database, go to ‘Other files/diagnosis_data.csv’
	  - If there is data, use ‘dummy_test.csv’
	  - Add some characters in the upload notes text area and hit submit
	  - You should be back to /data, if not manually go there. Click the get dataset button and go to either the top or bottom of the CSV to see the new rows added
4. Model button (code in views/model.html and blueprints/model.py):
  - Enter the values in the form to create a classifier of --> DecisionTreeClassifier(criterion = "gini", splitter = "random",  max_depth = 2, max_features = 6, random_state = 0, class_weight = "balanced")
  - Leave other values in the form to their default value
  - Submit to create a model to get a prediction for a feature set for
5. Predict button (code in views/predict.html, blueprints/prediction.py and views/results.html for the results)
  - Use the multiple prediction form, and ‘predict_this.csv’ for the CSV
  - After submitting the form, you should be on results page
	  - The top section is the plot of the trained model. The button below the plot is for downloading the dot file. This is to enter the dot file contents on a website like (http://www.webgraphviz.com), if the plot on the webpage is too small to make out.
	  - Under that is the feature impotences of the classifier
	  - Finally, the features sets with their predicted class and predicted probabilities of each class
### Finnie

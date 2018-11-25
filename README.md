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

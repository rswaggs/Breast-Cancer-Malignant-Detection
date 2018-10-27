Francis
  - [ ] User System 
    - [ ] Login
    - [ ] Authorization
    - [ ] Roles to prevent access to certain webpages for less qualified users
Ryan
Peter
- [ ] Create SQL commands to create database schema (do later after some work is complete)
- [ ] Make main template to extend from

- [ ] Patient search
  - [ ] Page to search basic health information on patients, see what predictions (if any) were run on them
- [ ] Data sharing
  - [ ] Userform to add single entry to dataset for training
  - [ ] Upload CSV to database functionality
    - [ ] Page to display who uploaded what, with a note on why, order by most recent uploads
  - [ ] Download CSV to database functionality for public utility / manual training
- [ ] Prediction system
  - [ ] Userform for one user cancer prediction
  - [ ] CSV file for multiple predictions
  - [ ] Function call to run model for prediction (decision tree)
  - [ ] Results
    - [ ] Plot of model in use / summary statistics (like model accuracy, top n-features)
    - [ ] Result predictions displayed below plot
  - [ ] Obtain testing data
    - [ ] Analyze features of dataset for statistical distributions
    - [ ] Randomly create new data points following observed statistical distributions for each variable
- [ ] Model training
  - [ ] Implement decision tree
    - [ ] 70% training set, 30% test set
    - [ ] Make sure model isn't overfitted
- [ ] Webpage with userform to enter parameter values to train the model with
  - [ ] Extra* Create gridsearch pipe to automatically train new models by finding the most optimal parameters

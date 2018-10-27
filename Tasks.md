## General
- [ ] Create SQL commands in a text file to create database schema and procedures (since stored procedures will not be in the code files)

## Francis
  - [ ] Make main template to extend from
  - [ ] User System 
    - [x] Login page
    - [ ] Authorization
    - [ ] Roles to prevent access to certain webpages for less qualified users
  - [ ] Patient search
    - [ ] Page to search basic health information on patients, see what predictions (if any) were run on them

## Ryan
- [ ] Data route
  - [ ] Test functionality
    - [ ] Download CSV from MySQL database
    - [ ] Upload CSV to MySQL database
    - [ ] Bind MySQL to HTML to display comments on who uploaded what CSVs, and why
    - [ ] Make the frontend HTML files pretty
    
## Peter
- [ ] Webpage route (maybe called /predict) with userform to enter parameter values to train the model with (or CSV or function, however we are assuming we're getting the data)
  - [ ] Userform for one user cancer prediction
  - [ ] CSV file for multiple predictions, or some function to pretend the data is coming for a network device (like x-ray)
  - [ ] Ryan can help create a function for random test values (since I partially worked on something like this, says Ryan), if it will help with the application
- [ ] Webpage route (maybe called /results) to display the results
  - [ ] Prediction results displayed

## Everyone
- [ ] Model training
  - [ ] Implement decision tree
    - [ ] 70% training set, 30% test set
    - [ ] Make sure model isn't overfitted
- [ ] Prediction system
  - [ ] Function call to run model for prediction (decision tree, maybe logistic regression if there's time) (hard code model in pickle object for now)
    
## Future tasks
- [ ] Webpage route (maybe called /models) to create new models within the application
  - Static or dynamic (this is where the /data route helps out, as the training data will be within the database)
    - [ ] Static: Assume user will know the model parameters, and will enter those in a userform for the model training process
    - [ ] Dynamic: Create gridsearch pipe to automatically train new models by finding the most optimal parameters (function will test the accuracy of different parameters, and will select the one that gives the best accuracy)
- [ ] Results webpage route extension
  - [ ] Plot of model in use / summary statistics (like model accuracy, top n-features)
  - [ ] Result predictions displayed below plot
- [ ] Upload to the cloud. This will allow the markers to fully appreciate our work and understand the underlining code.

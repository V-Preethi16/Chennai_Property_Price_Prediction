****This data science project series walks through step by step process of how to build a real estate price prediction website.****

    Step 1: Collect realtime data's for property price prediction using web scrapping method.Then convert that file to csv file. 
    Step 2: Load a .csv file dataset in jupyter notebook.Perform EDA (Explorary data analysis) on the dataset using boxplot,histplot,countplot,regplot and scatterplot.
    Step 3: Perform Z-score method to remove outliers which was detected in previous step.
    Step 4: After data cleaning, data's are splitted using train_test_split method from sklearn.
    Step 5: Train the data using linear regression model.
    Step 6: Generate Mean squared error(mse),R-squared error using linear regression model and random forest model.Compare both mse,R^2 values and found that linear regression model is 
            performing well compared to random forest.
    Step 7: Write a python flask server in Visual Studio Code(IDE) that uses the saved model to serve http requests and inreturn get response from server.
    Step 8: Build a website using html, css and javascript that allows user to enter area sqft value, select location and property type and it will call python flask server to retrieve the             predicted price. Then recent predicted prices with time & date will be stored in dashboard page and it also shows the highest predicted price within recent activity.*
****Technology and tools that this project covers,****
         -> Python
         -> matplotlib for data visualization
         -> numpy,pandas for data cleaning
         -> Sklearn for model building
         -> Flask framework for backend 
         -> Html,css and javascript for frontend
         -> joblib for loading .pkl model file
     
        
        

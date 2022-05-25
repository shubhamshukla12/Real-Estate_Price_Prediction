import numpy as np
import pickle
from flask import Flask, request, render_template

# Load ML model
model = pickle.load(open('Real_Estate_Price_Prediction_Project.pickle', 'rb')) 

# Create application
app = Flask(_name_,template_folder='templates')

# Bind home function to URL
@app.route('/')
def home():
    return render_template('index.html')

# Bind predict function to URL
@app.route('/predict', methods =['POST'])
def predict():
    
    # Put all form entries values in a list 
    features = [float(i) for i in request.form.values()]
    # Convert features to array
    array_features = [np.array(features)]
    # Predict features
    prediction = model.predict(array_features)
    
    output = prediction
    
    # Check the output values and retrive the result with html tag based on the value
    if output == 1:
        return render_template('index.html', 
                               result ="" )
    else:
        return render_template('index.html', 
                               result = "")

if _name_ == '_main_':
#Run the application
    app.run()
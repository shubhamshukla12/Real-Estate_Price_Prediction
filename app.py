# import numpy as np
# import pickle
# from flask import Flask, request, render_template

# # Load ML model
# model = pickle.load(open('Real_Estate_Price_Prediction_Project.pickle', 'rb')) 

# # Create application
# app = Flask(_name_,template_folder='templates')

# # Bind home function to URL
# @app.route('/')
# def home():
#     return render_template('index.html')

# # Bind predict function to URL
# @app.route('/predict', methods =['POST'])
# def predict():
    
#     # Put all form entries values in a list 
#     features = [float(i) for i in request.form.values()]
#     # Convert features to array
#     array_features = [np.array(features)]
#     # Predict features
#     prediction = model.predict(array_features)
    
#     output = prediction
    
#     # Check the output values and retrive the result with html tag based on the value
#     if output == 1:
#         return render_template('index.html', 
#                                result ="" )
#     else:
#         return render_template('index.html', 
#                                result = "")

# if _name_ == '_main_':
# #Run the application
#     app.run()

from flask import Flask, request, url_for, render_templates
import pickle
import numpy as np
import json

app = Flask(__name__)

app.config.update(
    dict(SECRET_KEY="powerful secretkey", WTF_CSRF_SECRET_KEY="a csrf secret key")
)

__locations = None
__data_columns = None
model = pickle.load(open("Real_Estate_Price_Prediction.pickle","rb"))

def get_estimated_price(input_json):
    try:
        loc_index = __data_columns.index(input_json['location'].lower())
    except:
        loc_index = -1
    x = np.zeros(244)
    x[0] = input_json['sqft']
    x[1] = input_json['bath']
    x[2] = input_json['bhk']
    if loc_index >= 0:
        x[loc_index] = 1
    result = round(model.predict([x])[0],2)
    return result

def get_location_names():
    return __locations

def load_saved_artifacts():
    print("Loading the saved artifacts...start !")
    global __data_columns
    global __locations
    global model

    with open("columns.json") as f:
        __data_columns = json.loads(f.read())["data_columns"]
        __locations = __data_columns[3:]

@app.route("/")
def index():
    return render_templates('index.html')


@app.route("/prediction", methods=["POST"])
def prediction():
    
    if request.method == 'POST':
        input_json = {
            "location": request.form['sLocation'],
            "sqft": request.form['Squareft'],
            "bhk": request.form['uiBHK'],
            "bath": request.form['uiBathrooms']
        }
        result = get_estimated_price(input_json)

        if result > 100:
            result = round(result/100, 2)
            result = str(result) + ' Crore'
        else:
            result = str(result) + ' Lakhs'
    return render_templates('prediction.html', result=result)

if __name__ == "__main__":
    print("Starting Python Flask Server")
    load_saved_artifacts()
    app.run(debug=True)

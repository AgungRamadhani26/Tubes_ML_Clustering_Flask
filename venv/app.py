import numpy as np
import os
import flask
import pickle
from flask import Flask, request, render_template, redirect, url_for

#create instance of Flask
app = Flask(__name__, template_folder='templates')

#picFolder
picFolder = os.path.join('static','img')
print(picFolder)
app.config['UPLOAD_FOLDER'] = picFolder

@app.route('/')
@app.route('/index')

#function to render the html page
def index():
    #upload image
    picture_main = os.path.join(app.config['UPLOAD_FOLDER'], 'cloudy.png')
    return render_template('index.html', user_image_main = picture_main)


#function to predict the output
def ValuePredictor(to_predict_list):
    to_predict = np.array(to_predict_list).reshape(1, 2)
    loaded_model = pickle.load(
        open("./model/model.pkl", "rb"))
    result = loaded_model.predict(to_predict)
    return result[0]

#function to get the input from the user
@app.route('/result', methods = ['POST'])
def result():
    if request.method == 'POST':
        picture = os.path.join(app.config['UPLOAD_FOLDER'], 'images.png')
        precipation = request.form['precipitation']
        temp_min = request.form['temp_max']
        to_predict_list = list(map(float, [precipation, temp_min]))
        result = ValuePredictor(to_predict_list)
        if int(result) == 0:
            prediction = 'low precipitation and low temperature (Cluster 1)'
        elif int(result) == 1:
            prediction = 'low precipitation and high temperature (Cluster 2)'
        elif int(result) == 2:
            prediction = 'high precipitation and normal temperature (Cluster 3)'
        return render_template("result.html", prediction=prediction, user_image_result = picture)

if __name__ == "__main__":
    app.run(debug=True)

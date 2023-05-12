import pickle # import pickle5 as pickle
from flask import Flask, request, app, jsonify, url_for, render_template, jsonify, request
import numpy as np # import pandas as pd
app = Flask(__name__)

regModel = pickle.load(open('regModel.pkl', 'rb'))
scalar = pickle.load(open('standard_scaler.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/predict_api', methods=['POST'])
def predict_api():
    data = request.json['data']
    # print("data ", data)
    print(np.array(list(data.values())).reshape(1, -1))
    # new_data = scalar.transform(np.array(list(data.values())).reshape(1, -1))
    new_data = np.array(list(data.values())).reshape(1, -1)
    output = regModel.predict(new_data)
    # print("output", output[0])  # since o/p is of 2-d array
    return jsonify(output[0])


@app.route('/predict', methods=['POST'])
def predict():
    # data = [float(x) for x in request.form.values()]
    # print("request.form ", request.form)
    # print("request.form2 ", request.form.values())
    data = [(x) for (x) in request.form.values()]
    # print("data ", data)
    # final_input = scalar.transform(np.array(data).reshape(1, -1))
    # final_input = scalar.transform(data.reshape(1, -1))
    # final_input = data
    # print("final_input ", final_input)
    # final_input = [float(i) for i in final_input]
    # print("final_input ", final_input)
    final_input = scalar.transform(np.array(data).reshape(1, -1))
    # final_input = np.array(data, dtype=float).reshape(1, -1)
    output = regModel.predict(final_input)[0]
    # output = "87"
    return render_template("home.html", prediction_text="The Employee Evaluation is:- The employee is in top {} percentile ".format(output))

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)

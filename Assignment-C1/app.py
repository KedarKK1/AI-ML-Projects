# import pandas as pd
# from sklearn import model_selection
# from sklearn.linear_model import LogisticRegression
# import pickle

# df = pd.read_csv("dataset.csv")
# print(df)

# import random
# k = list(random.randint(30, 100) for _ in range(100))
# for i in k:
    # print(i)
# X = array[:,0:8]
# Y = array[:,8]
# test_size = 0.33
# seed = 7
# X_train, X_test, Y_train, Y_test = model_selection.train_test_split(X, Y, test_size=test_size, random_state=seed)
# # Fit t he model on training set
# model = LogisticRegression()
# model.fit(X_train, Y_train)
# # save the model to disk
# filename = 'finalized_model.sav'
# pickle.dump(model, open(filename, 'wb'))
 
# # some time later...
 
# # load the model from disk
# loaded_model = pickle.load(open(filename, 'rb'))
# result = loaded_model.score(X_test, Y_test)
# print(result)

import pickle
# import pickle5 as pickle
from flask import Flask, request, app, jsonify, url_for, render_template, jsonify, request
import numpy as np
import pandas as pd

app = Flask(__name__)

regModel = pickle.load(open('regModel.pkl', 'rb'))
scalar = pickle.load(open('standard_scaler.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/predict_api', methods=['POST'])
def predict_api():
    data = request.json['data']
    print("data ", data)
    print(np.array(list(data.values())).reshape(1, -1))
    # new_data = scalar.transform(np.array(list(data.values())).reshape(1, -1))
    new_data = np.array(list(data.values())).reshape(1, -1)
    output = regModel.predict(new_data)
    print("output", output[0])  # since o/p is of 2-d array
    return jsonify(output[0])


@app.route('/predict', methods=['POST'])
def predict():
    # data = [float(x) for x in request.form.values()]
    print("request.form ", request.form)
    print("request.form2 ", request.form.values())
    data = [(x) for (x) in request.form.values()]
    # print("data ", data)
    # final_input = scalar.transform(np.array(data).reshape(1, -1))
    # final_input = scalar.transform(data.reshape(1, -1))
    # final_input = data
    final_input = np.array(data, dtype=float).reshape(1, -1)
    print("final_input ", final_input)
    # final_input = [float(i) for i in final_input]
    # print("final_input ", final_input)
    output = regModel.predict(final_input)[0]
    # output = "87"
    return render_template("home.html", prediction_text="The Employee Evaluation is {} ".format(output))

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)

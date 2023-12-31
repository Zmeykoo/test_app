import numpy as np
from flask import Flask, render_template, request, jsonify
import pickle

app = Flask(__name__)
model = pickle.load(open('model.pkl', 'rb'))


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/code')
def show_code():
    with open('app.py', 'r') as f:
        code = f.read()
    return render_template('app_code.html', code='app.py:\n{}'.format(code))


@app.route('/predict', methods=['POST'])
def predict():
    try:
        int_features = [int(x) for x in request.form.values()]
    except ValueError:
        return render_template('index.html', prediction_text='All input values should be integers')

    final_features = [np.array(int_features)]
    prediction = model.predict(final_features)

    output = round(prediction[0], 2)

    return render_template('index.html', prediction_text='Sales should be $ {}'.format(output))


@app.route('/results', methods=['POST'])
def results():

    data = request.get_json(force=True)
    prediction = model.predict([np.array(list(data.values()))])

    output = prediction[0]
    return jsonify(output)


if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, render_template, request
import joblib
import numpy as np

# ==========================
# LOAD TRAINED MODEL
# ==========================
model = joblib.load('linear_model_joblib')

app = Flask(__name__)

# ==========================
# ROUTES
# ==========================

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/contact')
def contact():
    return render_template("contact.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/project')
def project():
    return render_template("project.html")


# ==========================
# DICTIONARIES (ENCODING)
# ==========================

brand_dict = {
    'TVS':1, 'Royal Enfield':2, 'Triumph':3, 'Yamaha':4,
    'Honda':5, 'Hero':6, 'Bajaj':7, 'Suzuki':8,
    'Benelli':9, 'KTM':10, 'Mahindra':11, 'Kawasaki':12,
    'Ducati':13, 'Hyosung':14, 'Harley-Davidson':15,
    'Jawa':16, 'BMW':17, 'Indian':18, 'Rajdoot':19,
    'LML':20, 'Yezdi':21, 'MV':22, 'Ideal':23
}


# ==========================
# PREDICTION ROUTE
# ==========================

@app.route('/predict', methods=['GET', 'POST'])
def predict():

    if request.method == 'POST':

        # ===== GET FORM DATA =====
        brand_name = request.form['brand_name']
        owner = int(request.form['owner'])
        age = int(request.form['age'])
        power = int(request.form['power'])
        kms_driven = int(request.form['kms_driven'])

        print("Bike data received ✅")

        # ===== ENCODING =====
        brand_name = brand_dict[brand_name]

        # ===== FEATURE ORDER (MUST MATCH TRAINING) =====
        features = [[
            brand_name,
            owner,
            age,
            power,
            kms_driven
        ]]

        print("Features:", features)

        # ===== PREDICTION =====
        prediction = model.predict(features)[0]

        result = f"Estimated Bike Price: ₹ {round(prediction, 2)}"

        return render_template('project.html', prediction=result)

    # GET request
    return render_template('project.html')


# ==========================
# RUN APP
# ==========================
if __name__ == '__main__':
    app.run(debug=True)
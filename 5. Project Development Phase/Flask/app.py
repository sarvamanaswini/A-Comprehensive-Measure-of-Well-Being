# ====================================================================
# 1. IMPORT REQUIRED LIBRARIES
# ====================================================================
from flask import Flask, render_template, request, url_for
import pickle
import numpy as np

# ====================================================================
# 2. INITIALIZE FLASK APP & LOAD THE ML MODEL
# ====================================================================
app = Flask(__name__)

# Load the pre-trained Human Development Index prediction model
with open('HDI.pkl', 'rb') as file:
    model = pickle.load(file)

# ====================================================================
# 3. DEFINE APPLICATION ROUTES
# ====================================================================

@app.route('/')
def home():
    """
    Home Page Route
    Renders 'home.html' which serves as the introductory landing page.
    """
    return render_template('home.html')


@app.route('/predict_form')
def predict_form():
    """
    Form Page Route
    Renders 'indexnew.html' containing the feature input forms.
    """
    return render_template('indexnew.html')


@app.route('/predict', methods=['POST'])
def predict():
    """
    Prediction & Classification Route
    Extracts features, scales outputs if needed, categorizes development levels,
    and forwards final formatted strings to 'result.html'.
    """
    if request.method == 'POST':
        # Extract inputs securely from form submission tags
        country = request.form['country'] 
        life_exp = float(request.form['life_exp'])
        schooling = float(request.form['schooling'])
        gni = float(request.form['gni'])
        internet_users = float(request.form['internet_users'])
        
        # Build numerical feature configuration matrix
        features = np.array([[life_exp, schooling, gni, internet_users]])
        
        # Run calculation inference using the unpickled classifier pipeline
        prediction = model.predict(features)
        raw_output = prediction[0]
        
        # Dynamic Scaling Check: Converts values seamlessly if targets scaled out of 1000
        if raw_output > 1.0:
            raw_output = raw_output / 1000.0
            
        # Round value for standardized UI presentation 
        output = round(raw_output, 2)

        # Apply standard UNDP development tier classification boundaries
        if output < 0.55:
            category = "Low HDI"
        elif 0.55 <= output < 0.70:
            category = "Medium HDI"
        elif 0.70 <= output < 0.80:
            category = "High HDI"
        else:
            category = "Very High HDI"
            
        # Format exact summary payload string sent over to templates
        prediction_text = f"{category} {output:.2f}"
        
        return render_template('result.html', prediction_text=prediction_text)


if __name__ == '__main__':
    # Activate regional loop hosting back on local environment
    app.run(debug=True)
from flask import Flask, request, render_template
import numpy as np
import pickle

# Importing model and scaler
model =pickle.load(open('model.pkl', 'rb'))
sc = pickle.load(open('standscaler.pkl', 'rb'))
ms = pickle.load(open('minmaxscaler.pkl', 'rb'))

# Creating Flask app
app = Flask(__name__)

@app.route('/')
def index():
    return render_template("recommendation.html")

@app.route("/predict", methods=['POST'])
def predict():
    try:
        # Convert input values to float
        N = float(request.form['Nitrogen'])
        P = float(request.form['Phosphorus'])
        K = float(request.form['Potassium'])
        temp = float(request.form['Temperature'])
        humidity = float(request.form['Humidity'])
        ph = float(request.form['Ph'])
        rainfall = float(request.form['Rainfall'])

        # Create feature array
        feature_list =[N, P, K, temp, humidity, ph, rainfall]
        single_pred = np.array(feature_list).reshape(1,-1)

        # Apply scaling
        scaled_features = ms.transform(single_pred)
        final_fratures = sc.transform(scaled_features)
        prediction = model.predict(final_fratures)

        # Crop dictionary
        crop_dict = {
            1: "Rice", 2: "Maize", 3: "Jute", 4: "Cotton", 5: "Coconut", 6: "Papaya", 7: "Orange",
            8: "Apple", 9: "Muskmelon", 10: "Watermelon", 11: "Grapes", 12: "Mango", 13: "Banana",
            14: "Pomegranate", 15: "Lentil", 16: "Blackgram", 17: "Mungbean", 18: "Mothbeans",
            19: "Pigeonpeas", 20: "Kidneybeans", 21: "Chickpea", 22: "Coffee"
        }
        # Extract prediction result
        pred_value = int(prediction[0])  # Ensure prediction is an integer

        if pred_value in crop_dict:
            crop = crop_dict[pred_value]
            result = f"{crop} is the best crop to be cultivated right there."
        else:
            result = "Sorry, we could not determine the best crop to be cultivated with the provided data."

    except Exception as e:
        result = f"Error: {str(e)}"

    return render_template('result.html', result=result)

# Run Flask app
if __name__ == "__main__":
    app.run(debug=True)

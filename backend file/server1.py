from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import pandas as pd
import joblib
from datetime import datetime

app = Flask(__name__)

app.secret_key = 'your_secret_key'  # Replace with a secure key
# Load your model and preprocessor
rf_model = joblib.load('random_forest_regressor_model.pkl')
preprocessor = joblib.load('preprocessor.pkl')

# Extract the locations from the preprocessor
column_transformer = preprocessor.named_transformers_['cat']
locations = column_transformer.categories_[1].tolist()

# In-memory storage for recent activities and highest predicted prices
recent_activities = []
highest_predicted_prices = []
@app.route('/')
def home():
    return render_template('home.html')
@app.route('/login')
def login_register():
    return render_template('page2.html')

@app.route('/index')
def index():
    predicted_price = session.pop('predicted_price', None)
    selected_area_insqft = session.pop('selected_area_insqft', None)
    selected_property_type = session.pop('selected_property_type', None)
    selected_location = session.pop('selected_location', None)
    return render_template('index.html', locations=locations, predicted_price=predicted_price,
                           selected_area_insqft=selected_area_insqft, selected_property_type=selected_property_type,
                           selected_location=selected_location)


@app.route('/predict', methods=['POST'])
def predict():
    global highest_predicted_prices  # Declare highest_predicted_prices as global

    try:
        property_type = request.form.get('propertyType')
        area_insqft = float(request.form.get('areaInsqft', 0))
        location = request.form.get('location')

        # Validate the area in square feet
        if area_insqft <= 300:
            error_message = "Area sqft must be greater than 300."
            return render_template('index.html', locations=locations, error_message=error_message,
                                   selected_area_insqft=area_insqft, selected_property_type=property_type,
                                   selected_location=location)

        # Create a DataFrame for the input
        input_data = pd.DataFrame({
            'property_type': [property_type],
            'area_insqft': [area_insqft],
            'location': [location]
        })

        # Preprocess the input data
        input_data_preprocessed = preprocessor.transform(input_data)

        # Make prediction
        predicted_price = rf_model.predict(input_data_preprocessed)[0]
        predicted_price_formatted = f'Rs:{predicted_price:,.2f}'

        # Update recent activities
        activity = {
            'property_type': property_type,
            'area_insqft': area_insqft,
            'location': location,
            'predicted_price': predicted_price_formatted,
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        recent_activities.insert(0, activity)  # Add new activity to the beginning
        if len(recent_activities) > 10:  # Limit recent activities to the last 10 entries
            recent_activities.pop()

        # Update highest predicted prices
        highest_predicted_prices.append({
            'property_type': property_type,
            'location': location,
            'area_insqft': area_insqft,
            'predicted_price': predicted_price_formatted
        })
        # Sort by predicted price (descending) and limit to top 5
        highest_predicted_prices.sort(key=lambda x: float(x['predicted_price'].replace('Rs:', '').replace(',', '')), reverse=True)
        if len(highest_predicted_prices) > 5:
            highest_predicted_prices = highest_predicted_prices[:5]

        # Store prediction results in session
        session['predicted_price'] = predicted_price_formatted
        session['selected_area_insqft'] = area_insqft
        session['selected_property_type'] = property_type
        session['selected_location'] = location

        # Redirect to index page
        return redirect(url_for('index'))

    except Exception as e:
        print(f"Error in prediction: {e}")
        return render_template('index.html', locations=locations, error_message="An error occurred during prediction.",
                               selected_area_insqft=area_insqft, selected_property_type=property_type,
                               selected_location=location)

    except Exception as e:
        print(f"Error in prediction: {e}")
        return render_template('index.html', locations=locations, error_message="An error occurred during prediction.",
                               selected_area_insqft=area_insqft, selected_property_type=property_type,
                               selected_location=location)
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', recent_activities=recent_activities, highest_predicted_prices=highest_predicted_prices)

if __name__ == '__main__':
    app.run(debug=True)

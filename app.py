from flask import Flask, render_template, request, jsonify
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS to avoid cross-origin issues

# Your API key and URL
API_KEY = 'c2d41fd0a66937ce02e7ae5e'
API_URL = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/USD"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/currencies', methods=['GET'])
def get_currencies():
    """Fetch the list of available currencies from the API."""
    response = requests.get(API_URL)
    data = response.json()

    if data['result'] == 'success':
        currencies = list(data['conversion_rates'].keys())  # Extract currency codes
        return jsonify({'currencies': currencies})
    return jsonify({'error': 'Failed to fetch currencies.'}), 500

@app.route('/convert', methods=['POST'])
def convert():
    """Convert currency using the API."""
    data = request.get_json()
    from_currency = data.get('from_currency')
    to_currency = data.get('to_currency')
    amount = float(data.get('amount', 0))

    # Fetch the conversion rate from the API
    response = requests.get(API_URL)
    api_data = response.json()

    if api_data['result'] == 'success':
        conversion_rates = api_data['conversion_rates']
        from_rate = conversion_rates.get(from_currency)
        to_rate = conversion_rates.get(to_currency)

        if from_rate and to_rate:
            # Calculate the converted amount
            converted_amount = (amount / from_rate) * to_rate
            return jsonify({
                'converted_amount': round(converted_amount, 2),
                'to_currency': to_currency
            })
    return jsonify({'error': 'Conversion failed.'}), 400

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, request, jsonify
import json
import requests
import ast
import os
from dotenv import load_dotenv



load_dotenv()

app = Flask(__name__)

API_SANDBOX_TOKEN = os.getenv('SANDBOX_TOKEN')
AUTHORIZED_TOKENS = ast.literal_eval(os.getenv('AUTHORIZED_TOKENS'))


def check_imei(imei):
    url = "https://api.imeicheck.net/v1/checks"

    payload = json.dumps({
        "deviceId": imei,
        "serviceId": 12
        })
    
    headers = {
    'Authorization': f'Bearer {API_SANDBOX_TOKEN}',
    'Accept-Language': 'en',
    'Content-Type': 'application/json'
    }
    
    response = requests.request("POST", url, headers=headers, data=payload)

    return response.json()


@app.route('/api/check-imei', methods=['POST'])
def api_check_imei():
    data = request.json
    imei = str(data.get('imei'))
    token = str(data.get('token'))

    if not imei or not token:
        return jsonify({'error': 'IMEI and token are required'}), 400

    if token not in AUTHORIZED_TOKENS:
        return jsonify({'error': 'Unauthorized'}), 403

    imei_info = check_imei(imei)
    return jsonify(imei_info)


if __name__ == '__main__':
    app.run(debug=True)
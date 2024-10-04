from flask import Flask, request, jsonify
import hmac
import hashlib

app = Flask(__name__)

# Replace this secret key with the actual one from your Pesapal account
PESAPAL_CONSUMER_SECRET = "OuVah65aa8nlL4r8JwpHdoSRgcU="

# Endpoint for receiving IPN notifications from Pesapal
@app.route('/ipn', methods=['POST'])
def ipn():
    try:
        notification_data = request.get_json()

        # Extract necessary details from the notification
        pesapal_transaction_tracking_id = notification_data.get("pesapal_transaction_tracking_id")
        pesapal_merchant_reference = notification_data.get("pesapal_merchant_reference")
        pesapal_notification_type = notification_data.get("pesapal_notification_type")
        signature = notification_data.get("signature")

        # Validate the signature
        valid_signature = validate_pesapal_signature(notification_data, signature)

        if valid_signature:
            if pesapal_notification_type == "COMPLETED":
                # Handle payment success
                return jsonify({"status": "success", "message": "Payment processed successfully."}), 200
            elif pesapal_notification_type == "FAILED":
                # Handle payment failure
                return jsonify({"status": "failed", "message": "Payment failed."}), 200
        else:
            return jsonify({"status": "error", "message": "Invalid signature."}), 400

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

# Validate the Pesapal Signature
def validate_pesapal_signature(data, signature):
    """ Function to validate the HMAC signature from Pesapal """
    encoded_data = f"{data['pesapal_transaction_tracking_id']},{data['pesapal_merchant_reference']},{data['pesapal_notification_type']}".encode()
    calculated_signature = hmac.new(PESAPAL_CONSUMER_SECRET.encode(), encoded_data, hashlib.sha256).hexdigest()

    return hmac.compare_digest(calculated_signature, signature)

# Home route (you can add more routes as needed)
@app.route('/')
def home():
    return "Welcome to the Payment System!"

if __name__ == '__main__':
    app.run(debug=True, port=5000)


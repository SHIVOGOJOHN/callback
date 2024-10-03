from flask import Flask, request

app = Flask(__name__)

@app.route('/pesapal-callback', methods=['POST'])
def pesapal_callback():
    data = request.get_json()
    print("Callback Data:", data)

    # Handle the payment status
    transaction_status = data.get("status")
    if transaction_status == "COMPLETED":
        print("Payment completed successfully.")
    elif transaction_status == "FAILED":
        print("Payment failed.")
    elif transaction_status == "PENDING":
        print("Payment is pending.")

    return "OK", 200

@app.route('/pesapal-ipn', methods=['POST'])
def pesapal_ipn():
    data = request.get_json()
    print("IPN Data:", data)

    # Handle the IPN notification
    transaction_status = data.get("status")
    transaction_reference = data.get("order_tracking_id")

    if transaction_status == "COMPLETED":
        print(f"Transaction {transaction_reference} completed successfully.")
    elif transaction_status == "FAILED":
        print(f"Transaction {transaction_reference} failed.")
    elif transaction_status == "PENDING":
        print(f"Transaction {transaction_reference} is pending.")

    return "OK", 200

if __name__ == '__main__':
    app.run(port=5000)


from flask import Flask, request, jsonify
from twilio.rest import Client
import os

app = Flask(__name__)

# Twilio credentials from environment or hardcoded for demo
account_sid = "DWW583B7G5P7CEUQNCAKKZ6W"
auth_token = "US2374228dcc0e7a48d1a1060e72b233ed"
twilio_number = "+18883625982"

client = Client(account_sid, auth_token)

@app.route('/sms-alert', methods=['POST'])
def sms_alert():
    data = request.json
    pickup = data.get('pickup_zip')
    dropoff = data.get('dropoff_zip')
    item = data.get('item_type')
    size = data.get('item_size')
    user_phone = data.get('user_phone')

    # Estimate logic (simplified)
    base_price = 30
    distance_est = abs(int(pickup[:3]) - int(dropoff[:3])) * 1.5
    size_modifier = {"Small": 0, "Medium": 20, "Large": 40}.get(size, 0)
    estimated = base_price + distance_est + size_modifier

    # Send SMS to you
    message = f"New Estimate Request: {item} ({size}) from {pickup} to {dropoff}. Est. ${estimated:.2f}"
    client.messages.create(
        body=message,
        from_=twilio_number,
        to="+1YOURPERSONALNUMBER"  # <-- replace with your real cell
    )

    # Optional: Text back to customer
    if user_phone:
        client.messages.create(
            body=f"Thanks for your request! We estimate ${estimated:.2f} for your move. We'll confirm everything on the call.",
            from_=twilio_number,
            to=user_phone
        )

    return jsonify({"success": True, "estimate": estimated})

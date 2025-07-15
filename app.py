from flask import Flask, render_template, request, jsonify
from flask_pymongo import PyMongo
from datetime import datetime
import os

app = Flask(__name__)

# Get MongoDB URI from environment variable
mongo_uri = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/portfolio_db')
app.config["MONGO_URI"] = mongo_uri
mongo = PyMongo(app)

# Root route to serve portfolio
@app.route('/')
def home():
    return render_template('index.html')

# Contact form submission endpoint
@app.route('/submit_contact', methods=['POST'])
def submit_contact():
    data = request.json
    
    # Create contact document
    contact = {
        'name': data['name'],
        'email': data['email'],
        'subject': data['subject'],
        'message': data['message'],
        'timestamp': datetime.utcnow()
    }
    
    # Insert into MongoDB
    result = mongo.db.contacts.insert_one(contact)
    
    if result.inserted_id:
        return jsonify({
            'success': True,
            'message': 'Thank you for your message! I will get back to you soon.'
        }), 200
    else:
        return jsonify({
            'success': False,
            'message': 'Failed to send message. Please try again.'
        }), 500

# Only run directly in development mode
if __name__ == '__main__':
    if os.environ.get('FLASK_ENV') == 'development':
        app.run(debug=True)

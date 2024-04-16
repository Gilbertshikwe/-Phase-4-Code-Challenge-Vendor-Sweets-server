from dotenv import load_dotenv

load_dotenv()
import os
from models import db, Sweet, Vendor, VendorSweet
from flask_migrate import Migrate #type:ignore
from flask import Flask, request, jsonify #type:ignore 
from flask_cors import CORS #type:ignore

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DATABASE_URL", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(app)

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return '<h1>Code challenge</h1>'

@app.route('/vendors', methods=['GET'])
def get_vendors():
    vendors = Vendor.query.all()
    return jsonify([vendor.to_json() for vendor in vendors])

@app.route('/vendors/<int:vendor_id>', methods=['GET'])
def get_vendor(vendor_id):
    vendor = Vendor.query.get(vendor_id)
    if vendor:
        return jsonify(vendor.to_json())
    else:
        return jsonify({'error': 'Vendor not found'}), 404

@app.route('/sweets', methods=['GET'])
def get_sweets():
    sweets = Sweet.query.all()
    return jsonify([sweet.to_json() for sweet in sweets])

@app.route('/sweets/<int:sweet_id>', methods=['GET'])
def get_sweet(sweet_id):
    sweet = Sweet.query.get(sweet_id)
    if sweet:
        return jsonify(sweet.to_json())
    else:
        return jsonify({'error': 'Sweet not found'}), 404

@app.route('/vendor_sweets', methods=['POST'])
def create_vendor_sweet():
    data = request.get_json()
    vendor_id = data.get('vendor_id')
    sweet_id = data.get('sweet_id')
    price = data.get('price')

    vendor = Vendor.query.get(vendor_id)
    sweet = Sweet.query.get(sweet_id)

    if vendor and sweet:
        vendor_sweet = VendorSweet(price=price, vendor_id=vendor_id, sweet_id=sweet_id)
        db.session.add(vendor_sweet)
        db.session.commit()
        return jsonify(vendor_sweet.to_json()), 201
    else:
        return jsonify({'errors': ['Vendor or Sweet not found']}), 400

@app.route('/vendor_sweets/<int:vendor_sweet_id>', methods=['DELETE'])
def delete_vendor_sweet(vendor_sweet_id):
    vendor_sweet = VendorSweet.query.get(vendor_sweet_id)
    if vendor_sweet:
        db.session.delete(vendor_sweet)
        db.session.commit()
        return jsonify({}), 200
    else:
        return jsonify({'error': 'VendorSweet not found'}), 404

if __name__ == '__main__':
    app.run(port=5555, debug=True)


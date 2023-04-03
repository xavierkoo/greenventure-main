from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from os import environ

app = Flask(__name__)

# voucherDB database
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')  or "http://localhost:5101/voucher"         
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app)

class Voucher(db.Model):
    __tablename__ = 'voucher'
    #Specify the columns in the voucher table as attributes in our Voucher class using SQLAlchemy's column types, such as db.Integer and db.String.
    voucherID = db.Column(db.Integer, primary_key=True) 
    value = db.Column(db.Integer, nullable=False)
    merchant_name = db.Column(db.String(50), nullable=False)
    voucher_name = db.Column(db.String(50), nullable=False)
    voucher_code = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(50), nullable=False)
    pointsRequired = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)


    def __init__(self, voucherID, value,voucherName, merchantName,voucherCode, description, pointsRequired,quantity):
        self.pointsRequired = pointsRequired
        self.voucherID = voucherID
        self.value = value
        self.merchant_name = merchantName
        self.voucher_code = voucherCode
        self.voucher_name = voucherName
        self.description = description
        self.quantity = quantity
        


    def json(self):
        return {"voucherID": self.voucherID, "value": self.value, "merchantName": self.merchant_name,"voucherName":self.voucher_name , "voucherCode":self.voucher_code ,"description": self.description, "pointsRequired": self.pointsRequired,"quantity": self.quantity}



#Retrieve all vouchers available
@app.route("/voucher")
def get_all():
    allVoucher = Voucher.query.all()
    if len(allVoucher):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "vouchers": [voucher.json() for voucher in allVoucher]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no vouchers."
        }
    ), 404

# Find particular voucher using voucher ID
@app.route("/voucher/<int:voucherID>")
def find_voucher_by_voucherId(voucherID):
    voucher = Voucher.query.filter_by(voucherID=voucherID).first() #green one is table voucherID. Pink one is the input
    if voucher:
        return jsonify(
            {
                "code": 200,
                "data": voucher.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Voucher not found."
        }
    ), 404

# Reduce the number of vouchers available when a user redeem
@app.route("/voucher/<string:voucherCode>", methods=['PATCH'])
def voucherMinus(voucherCode):
    voucher = Voucher.query.filter_by(voucher_code=voucherCode).first()
    if voucher:
        #Reduce voucher quantity by 1
        voucher.quantity = voucher.quantity-1
        db.session.commit()
        return jsonify(
            {
                "code": 200,
                "data": voucher.json(),
                "message": "Voucher quantity reduce by 1."
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Voucher not found."
        }
    ), 404




if __name__ == '__main__':
     app.run(host='0.0.0.0', port=5101, debug=True)

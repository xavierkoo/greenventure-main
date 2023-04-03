from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from os import environ
app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost:3306/walletDB'
# export dbURL=mysql+mysqlconnector://root:root@localhost:3306/walletDB
# docker build -t mauriceho/wallet:1.0 ./
# docker run -p 5102:5102 -e dbURL=mysql+mysqlconnector://is213@host.docker.internal:3306/walletDB mauriceho/wallet:1.0

app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app)  

class Wallet(db.Model):
    __tablename__ = 'WALLET'
    walletID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userID = db.Column(db.String(50), nullable=False)
    points_remaining = db.Column(db.Integer, nullable=False)

    def __init__(self, userID, points_remaining):
        self.userID = userID
        self.points_remaining = points_remaining

    def json(self):
        return {"walletID": self.walletID, "userID": self.userID, "points_remaining": self.points_remaining}
    

class Walletvoucher(db.Model):
    _tablename_ = 'WALLETVOUCHER'
    walletID = db.Column(db.Integer, primary_key=True)
    voucherID = db.Column(db.String(20), primary_key=True)
    voucher_code = db.Column(db.String(20), primary_key=True)
    used = db.Column(db.Boolean)

    def __init__(self, walletID, voucherID, voucher_code, used):
        self.walletID = walletID
        self.voucherID = voucherID
        self.voucher_code = voucher_code
        self.used = used

    def json(self):
        return {"walletID": self.walletID, "voucherID": self.voucherID, "voucher_code": self.voucher_code, "used": self.used}
    

'''Add a voucher'''
# @app.route("/walletVoucher", methods=["POST"])
# def add_wallet_voucher():
#     data = request.get_json()
#     print(data)
#     walletID = data['walletID']
#     voucherID = data['voucherID']
#     voucher_code = data['voucher_code']
#     used = data['used']
#     WALLETVOUCHER = Walletvoucher(walletID, voucherID, voucher_code, used)
#     try:
#         db.session.add(WALLETVOUCHER)
#         db.session.commit()
#     except Exception as e:
#         return jsonify(
#             {
#                 "code": 500,
#                 "data": {
#                     "voucherID": voucherID
#                 }, 
#                 "message": "An error occurred adding the voucher into wallet." + str(e)
#             }
#         ), 500
#     return jsonify(
#         {
#             "code": 201,
#             "data": WALLETVOUCHER.json()
#         }
#     ), 201
@app.route("/wallet/adduser", methods=["POST"])
def add_wallet():
    data = request.get_json()

    WALLET = Wallet( data['userID'], points_remaining=0)
    try:
        db.session.add(WALLET)
        db.session.commit()
    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "voucherID": data['userID']
                }, 
                "message": "An error occurred adding the user into wallet." + str(e)
            }
        ), 500
    return jsonify(
        {
            "code": 201,
            "data": WALLET.json()
        }
    ), 201


'''Get all voucher in wallet'''
@app.route("/walletVoucher/<int:walletID>")
def get_voucher_ids(walletID):
    vouchers = Walletvoucher.query.filter_by(walletID=walletID).all()
    voucher_info = [{'voucherID': voucher.voucherID, 'voucher_code': voucher.voucher_code, 'used': voucher.used} for voucher in vouchers]
    return jsonify(
        {
            "code": 200,
            "voucher": voucher_info
        }
    )


'''Show user wallet'''
@app.route('/wallet/<int:user_id>')
def get_user_wallet(user_id):
    wallet = Wallet.query.filter_by(userID=user_id).first()
    if wallet:
            return jsonify({
                "code": 200,
                "walletID": wallet.walletID,
                "userID": wallet.userID,
                "points_remaining": wallet.points_remaining
            }
        ),200
    return jsonify({
        "message": "Wallet not found for the user.",
        "code": 404
    }), 404

'''use'''
@app.route('/wallet/use/<int:walletID>/<string:voucherCode>', methods=['PATCH'])
def mark_voucher_as_used(walletID, voucherCode):
    WALLETVOUCHER = Walletvoucher.query.filter_by(walletID=walletID, voucher_code=voucherCode).first()
    if WALLETVOUCHER:
        WALLETVOUCHER.used = True
        db.session.commit()
        return jsonify(
            {
                'code': 200,
                'message': f'Voucher {voucherCode} has been marked as used.'
            }
        ), 200
    return jsonify(
        {
            'code': 404,
            'message': 'Voucher not found.'
        }
    ), 404

'''add points in to wallet'''
@app.route('/wallet/addpoints', methods=['PATCH'])
def add_points_wallet():
    data = request.get_json()
    points_remaining = data['points_remaining']
    wallet_id = data['walletID']
    wallet = Wallet.query.filter_by(walletID=wallet_id).first()
    if wallet:
        wallet.points_remaining += points_remaining
        db.session.commit()
        return jsonify(
            {
                'code': 200,
                'message': f'{points_remaining} have been added to wallet'
            }
        ), 200
    return jsonify(
        {
            'code': 404,
            'message': 'wallet not found.'
        }
    ), 404

@app.route('/wallet', methods=['POST'])
def verify_and_exchange_points():
    # Find user's wallet by user ID
    data = request.get_json()
    user_ID = data['user_ID']
    voucherID = data['voucherID']
    voucher_code = data['voucher_code']
    voucher_amount = data['voucher_amount']

    wallet = Wallet.query.filter_by(userID=user_ID).first()
    if not wallet:
        return jsonify({
            'code': 404,
            'message': f"Wallet not found for user ID: {user_ID}"
        }), 404
    
    # Check if user has enough points to exchange for voucher
    if wallet.points_remaining < voucher_amount:
        return jsonify({
            'code': 400,
            'message': f"Not enough points remaining in wallet ID: {wallet.walletID} for exchange."
        }), 400
    
    wallet.points_remaining -= voucher_amount
    WALLETVOUCHER = Walletvoucher(wallet.walletID, voucherID, voucher_code, used = False)
    try:
        db.session.add(WALLETVOUCHER)
        db.session.commit()
    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "voucherID": voucherID
                }, 
                "message": "An error occurred adding the voucher into wallet." + str(e)
            }
        ), 500
    return jsonify(
        {
            "code": 201,
            "data": WALLETVOUCHER.json(),
            'message': f"{voucher_amount} points have been exchanged for voucher ID: {voucherID}"
        }
    ), 201
    


  

# @app.route('/wallet/<int:user_id>&<int:voucher_id>&<int:points_earned>', methods=['PATCH'])
# def verify_and_exchange_points(user_id, voucher_id, points_earned):
#     # Find user's wallet by user ID
#     wallet = Wallet.query.filter_by(userID=user_id).first()
#     if not wallet:
#         return jsonify({
#             'code': 404,
#             'message': f"Wallet not found for user ID: {user_id}"
#         }), 404
    
#     # Check if user has enough points to exchange for voucher
#     if wallet.points_remaining < points_earned:
#         return jsonify({
#             'code': 400,
#             'message': f"Not enough points remaining in wallet ID: {wallet.walletID} for exchange."
#         }), 400
    
#     # Find wallet voucher by wallet ID and voucher ID
#     WALLETVOUCHER = Walletvoucher.query.filter_by(walletID=wallet.walletID, voucherID=voucher_id).first()
#     if not WALLETVOUCHER:
#         return jsonify({
#             'code': 404,
#             'message': f"Wallet voucher not found for wallet ID: {wallet.walletID} and voucher ID: {voucher_id}"
#         }), 404
    
#     # Verify voucher code
#     if WALLETVOUCHER.voucher_code != 'VALID_CODE':
#         return jsonify({
#             'code': 400,
#             'message': f"Invalid voucher code for voucher ID: {voucher_id}"
#         }), 400
    
#     # Mark voucher as used
#     WALLETVOUCHER.used = True
    
#     # Update user's wallet points
#     wallet.points_remaining -= points_earned
    
#     # Commit changes to database
#     db.session.commit()
    
#     return jsonify({
#         'code': 200,
#         'message': f"{points_earned} points have been exchanged for voucher ID: {voucher_id}"
#     }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5102, debug=True)

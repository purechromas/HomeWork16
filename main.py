from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from data import users, orders, offers

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db: SQLAlchemy = SQLAlchemy(app)

with app.app_context():
    class User(db.Model):
        __tablename__ = 'user'

        id = db.Column(db.Integer, primary_key=True)
        first_name = db.Column(db.Text())
        last_name = db.Column(db.Text())
        age = db.Column(db.Integer)
        email = db.Column(db.Text, unique=True)
        role = db.Column(db.Text)
        phone = db.Column(db.Text, unique=True)


    class Order(db.Model):
        __tablename__ = 'order'

        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.Text())
        description = db.Column(db.Text())
        start_date = db.Column(db.Text)
        end_date = db.Column(db.Text)
        address = db.Column(db.Text)
        price = db.Column(db.Numeric)
        customer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
        executor_id = db.Column(db.Integer, db.ForeignKey('user.id'))


    class Offer(db.Model):
        __tablename__ = 'offer'

        id = db.Column(db.Integer, primary_key=True)
        order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
        executor_id = db.Column(db.Integer, db.ForeignKey('user.id'))

        user = db.relationship('User')
        order = db.relationship('Order')

    db.create_all()


with app.app_context():
    for user in users:
        user_ = User(**user)
        db.session.add(user_)
        db.session.commit()

    for order in orders:
        order_ = Order(**order)
        db.session.add(order_)
        db.session.commit()

    for offer in offers:
        offer_ = Offer(**offer)
        db.session.add(offer_)
        db.session.commit()


def get_all_users():
    """RETURNING ALL USERS FROM DATA BASE"""
    data = User.query.all()
    result = []
    for user_data in data:
        result.append(
            {
                'id': user_data.id,
                'first_name': user_data.first_name,
                'last_name': user_data.last_name,
                'age': user_data.age,
                'email': user_data.email,
                'role': user_data.role,
                'phone': user_data.phone,
            }
        )
    return result


def get_all_offers():
    """RETURNING ALL OFFERS FROM DATA BASE"""
    data = Offer.query.all()
    result = []
    for offer_data in data:
        result.append(
            {
                'id': offer_data.id,
                'order_id': offer_data.order_id,
                'executor_id': offer_data.executor_id,
            }
        )
    return result


def get_all_orders():
    """RETURNING ALL ORDERS FROM DATA BASE"""
    data = Order.query.all()
    result = []
    for order_data in data:
        result.append(
            {
                'id': order_data.id,
                'name': order_data.name,
                'description': order_data.description,
                'start_date': order_data.start_date,
                'end_date': order_data.end_date,
                'address': order_data.address,
                'price': order_data.price,
                'customer_id': order_data.customer_id,
                'executor_id': order_data.executor_id,
            }
        )
    return result


@app.route('/users', methods=['GET', 'POST'])
def users():
    if request.method == 'GET':
        return jsonify(get_all_users())
    else:
        request_data = request.json
        new_user = User(**request_data)
        db.session.add(new_user)
        db.session.commit()
        return 'Post was successful'


@app.route('/users/<int:pk>', methods=['GET', 'PUT', 'DELETE'])
def get_user(pk):
    user = User.query.get(pk)
    if request.method == 'GET':
        result = []
        result.append(
            {
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'age': user.age,
                'email': user.email,
                'role': user.role,
                'phone': user.phone,
            }
        )
        return jsonify(result)
    elif request.method == 'DELETE':
        db.session.delete(user)
        db.session.commit()
        return "Delete was successful"
    else:
        user_data = request.json
        user.first_name = user_data['first_name']
        user.last_name = user_data['last_name']
        user.age = user_data['age']
        user.email = user_data['email']
        user.role = user_data['role']
        user.phone = user_data['phone']
        return "Update was successful"


@app.route('/orders', methods=['GET', 'POST'])
def order():
    if request.method == 'GET':
        return jsonify(get_all_orders())
    else:
        request_data = request.json
        new_order = Order(**request_data)
        db.session.add(new_order)
        db.session.commit()
        return 'Post was successful'


@app.route('/orders/<int:pk>', methods=['GET', 'PUT', 'DELETE'])
def get_order(pk):
    order = Order.query.get(pk)
    if request.method == 'GET':
        result = []
        result.append(
            {
                'id': order.id,
                'name': order.name,
                'description': order.description,
                'start_date': order.start_date,
                'end_date': order.end_date,
                'address': order.address,
                'price': order.price,
                'customer_id': order.customer_id,
                'executor_id': order.executor_id,
            }
        )
        return jsonify(result)
    elif request.method == 'DELETE':
        db.session.delete(order)
        db.session.commit()
        return "Delete was successful"
    else:
        order_data = request.json
        order.name = order_data['name']
        order.description = order_data['description']
        order.start_date = order_data['start_date']
        order.end_date = order_data['end_date']
        order.address = order_data['address']
        order.price = order_data['price']
        order.customer_id = order_data['customer_id']
        order.executor_id = order_data['executor_id']
        return "Update was successful"


@app.route('/offers', methods=['GET', 'POST'])
def offers():
    if request.method == 'GET':
        return jsonify(get_all_offers())
    else:
        request_data = request.json
        new_offer = Offer(**request_data)
        db.session.add(new_offer)
        db.session.commit()
        return 'Post was successful'


@app.route('/offers/<int:pk>', methods=['GET', 'PUT', 'DELETE'])
def get_offers(pk):
    offer = Offer.query.get(pk)
    if request.method == 'GET':
        result = []
        result.append(
            {
                'id': offer.id,
                'order_id': offer.order_id,
                'executor_id': offer.executor_id,
            }
        )
        return jsonify(result)
    elif request.method == 'DELETE':
        db.session.delete(offer)
        db.session.commit()
        return "Delete was successful"
    else:
        offer_data = request.json
        offer.order_id = offer_data['order_id']
        offer.executor_id = offer_data['executor_id']
        return "Update was successful"


if __name__ == '__main__':
    app.run()

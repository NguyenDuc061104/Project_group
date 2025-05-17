from extensions import db 

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    teddy_id = db.Column(db.Integer, db.ForeignKey('teddy.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    price = db.Column(db.Integer, nullable=False)
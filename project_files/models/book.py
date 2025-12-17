from extensions import db


class Book(db.Model):
    __tablename__ = "books"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text)

    carts = db.relationship("Cart", backref="book", lazy=True)
    orders = db.relationship("Order", backref="book", lazy=True)

    def __repr__(self):
        return f"<Book {self.title}>"

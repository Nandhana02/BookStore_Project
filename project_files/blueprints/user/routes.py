from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from extensions import db
from models.book import Book
from models.cart import Cart
from models.order import Order
from . import user_bp
from sqlalchemy import func

@user_bp.route("/", methods=["GET"])
@login_required
def home():
    search_query = request.args.get("search", "").strip().lower()

    books = Book.query.all()

    if search_query:
        words = search_query.split()

        def matches(book):
            text = f"{book.title} {book.author}".lower()
            return all(word in text for word in words)

        books = [book for book in books if matches(book)]

    return render_template("user/home.html", books=books)



@user_bp.route("/add-to-cart/<int:book_id>")
@login_required
def add_to_cart(book_id):
    book = Book.query.get_or_404(book_id)

    if book.quantity <= 0:
        flash("Book out of stock.", "danger")
        return redirect(url_for("user.home"))

    cart_item = Cart.query.filter_by(
        user_id=current_user.id,
        book_id=book.id
    ).first()

    if cart_item:
        if cart_item.quantity < book.quantity:
            cart_item.quantity += 1
        else:
            flash("Not enough stock available.", "warning")
    else:
        cart_item = Cart(
            user_id=current_user.id,
            book_id=book.id,
            quantity=1
        )
        db.session.add(cart_item)

    db.session.commit()
    flash("Book added to cart.", "success")
    return redirect(url_for("user.home"))


@user_bp.route("/cart")
@login_required
def view_cart():
    cart_items = Cart.query.filter_by(user_id=current_user.id).all()
    total = sum(item.book.price * item.quantity for item in cart_items)
    return render_template("user/cart.html", cart_items=cart_items, total=total)
@user_bp.route("/checkout")
@login_required
def checkout():
    cart_items = Cart.query.filter_by(user_id=current_user.id).all()

    if not cart_items:
        flash("Cart is empty.", "warning")
        return redirect(url_for("user.home"))

    for item in cart_items:
        book = item.book

        if item.quantity > book.quantity:
            flash(f"Not enough stock for {book.title}.", "danger")
            return redirect(url_for("user.view_cart"))

        # Reduce inventory
        book.quantity -= item.quantity

        # Create order
        order = Order(
            user_id=current_user.id,
            book_id=book.id,
            quantity=item.quantity,
            status="Purchased"
        )
        db.session.add(order)

        # Remove from cart
        db.session.delete(item)

    db.session.commit()
    flash("Purchase successful!", "success")
    return redirect(url_for("user.orders"))
@user_bp.route("/orders")
@login_required
def orders():
    orders = Order.query.filter_by(user_id=current_user.id).all()
    return render_template("user/orders.html", orders=orders)


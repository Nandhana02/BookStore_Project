# admin routes will be added here
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from extensions import db
from models.book import Book
from . import admin_bp


def admin_required(func):
    from functools import wraps

    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin():
            flash("Admin access required.", "danger")
            return redirect(url_for("auth.login"))
        return func(*args, **kwargs)

    return wrapper


@admin_bp.route("/dashboard")
@login_required
@admin_required
def dashboard():
    books = Book.query.all()
    return render_template("admin/dashboard.html", books=books)


@admin_bp.route("/add", methods=["GET", "POST"])
@login_required
@admin_required
def add_book():
    if request.method == "POST":
        book = Book(
            title=request.form["title"],
            author=request.form["author"],
            category=request.form["category"],
            price=float(request.form["price"]),
            quantity=int(request.form["quantity"]),
            description=request.form.get("description"),
        )

        db.session.add(book)
        db.session.commit()
        flash("Book added successfully.", "success")
        return redirect(url_for("admin.dashboard"))

    return render_template("admin/add_book.html")


@admin_bp.route("/edit/<int:book_id>", methods=["GET", "POST"])
@login_required
@admin_required
def edit_book(book_id):
    book = Book.query.get_or_404(book_id)

    if request.method == "POST":
        book.title = request.form["title"]
        book.author = request.form["author"]
        book.category = request.form["category"]
        book.price = float(request.form["price"])
        book.quantity = int(request.form["quantity"])
        book.description = request.form.get("description")

        db.session.commit()
        flash("Book updated successfully.", "success")
        return redirect(url_for("admin.dashboard"))

    return render_template("admin/edit_book.html", book=book)


@admin_bp.route("/delete/<int:book_id>")
@login_required
@admin_required
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    flash("Book deleted.", "info")
    return redirect(url_for("admin.dashboard"))
from models.order import Order
from models.user import User


@admin_bp.route("/orders")
@login_required
@admin_required
def view_orders():
    orders = Order.query.all()
    return render_template("admin/orders.html", orders=orders)


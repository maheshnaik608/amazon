
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "amazon-shopping-demo-key"

products = [
    {"id": 1, "name": "Smartphone", "price": 14999,
     "category": "Electronics", "emoji": "📱"},
    {"id": 2, "name": "Laptop", "price": 45999,
     "category": "Electronics", "emoji": "💻"},
    {"id": 3, "name": "Headphones", "price": 1999,
     "category": "Electronics", "emoji": "🎧"},
    {"id": 4, "name": "Running Shoes", "price": 2499,
     "category": "Fashion", "emoji": "👟"},
    {"id": 5, "name": "Smart Watch", "price": 3499,
     "category": "Electronics", "emoji": "⌚"},
    {"id": 6, "name": "Backpack", "price": 1299,
     "category": "Fashion", "emoji": "🎒"},
]


@app.route("/")
def home():
    search = request.args.get("search", "").strip().lower()

    filtered_products = [
        p for p in products
        if search in p["name"].lower()
        or search in p["category"].lower()
    ]

    cart = session.get("cart", {})
    cart_count = sum(cart.values())

    return render_template(
        "index.html",
        products=filtered_products,
        cart_count=cart_count,
        search=search
    )


@app.route("/add/<int:product_id>", methods=["POST"])
def add_to_cart(product_id):
    if any(p["id"] == product_id for p in products):
        cart = session.get("cart", {})
        key = str(product_id)
        cart[key] = cart.get(key, 0) + 1
        session["cart"] = cart

    return redirect(url_for("home"))


@app.route("/cart")
def view_cart():
    cart = session.get("cart", {})
    items = []
    total = 0

    for product in products:
        quantity = cart.get(str(product["id"]), 0)
        if quantity:
            subtotal = product["price"] * quantity
            items.append({
                **product,
                "quantity": quantity,
                "subtotal": subtotal
            })
            total += subtotal

    return render_template(
        "cart.html",
        items=items,
        total=total,
        cart_count=sum(cart.values())
    )


@app.route("/remove/<int:product_id>", methods=["POST"])
def remove_from_cart(product_id):
    cart = session.get("cart", {})
    cart.pop(str(product_id), None)
    session["cart"] = cart
    return redirect(url_for("view_cart"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

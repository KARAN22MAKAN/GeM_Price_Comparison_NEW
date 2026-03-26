"""
GeM Price Comparison — Flask Backend
Run: python app.py
Then open http://localhost:8000
"""

from flask import Flask, request, jsonify, send_from_directory, abort
from datetime import date
import os
import database as db

app = Flask(__name__, static_folder="static")

# ── Startup ───────────────────────────────────────────────────────────────────
db.init_db()
db.seed_db()


# ── Frontend routes ───────────────────────────────────────────────────────────
@app.route("/")
def index():
    return app.send_static_file("index.html")


@app.route("/admin")
def admin():
    return send_from_directory("static", "admin.html")


@app.route("/static/<path:filename>")
def static_files(filename):
    return send_from_directory("static", filename)


# ── Public API ────────────────────────────────────────────────────────────────
@app.route("/api/search")
def search():
    q = request.args.get("q", "").strip()
    if not q:
        return jsonify({"error": "Query required"}), 400

    results = db.search_products(q)

    # Find overall cheapest across all results
    all_prices = [p for r in results for p in r["prices"]]
    overall_cheapest = None
    if all_prices:
        cp = min(all_prices, key=lambda x: x["price"])
        for r in results:
            for p in r["prices"]:
                if p["price"] == cp["price"] and p["platform"] == cp["platform"]:
                    overall_cheapest = {
                        **cp,
                        "product_name": r["name"],
                        "product_image": r["image_url"],
                    }
                    break
            if overall_cheapest:
                break

    return jsonify({
        "query": q,
        "total": len(results),
        "results": results,
        "overall_cheapest": overall_cheapest,
    })


@app.route("/api/stats")
def stats():
    return jsonify(db.get_stats())


@app.route("/api/categories")
def categories():
    return jsonify(db.get_categories())


# ── Admin API — Products ──────────────────────────────────────────────────────
@app.route("/api/admin/products", methods=["GET"])
def admin_list_products():
    return jsonify(db.get_all_products())


@app.route("/api/admin/products", methods=["POST"])
def admin_create_product():
    body = request.get_json(force=True)
    name = (body.get("name") or "").strip()
    if not name:
        return jsonify({"error": "name is required"}), 400
    try:
        category_id = int(body.get("category_id", 1))
    except (ValueError, TypeError):
        return jsonify({"error": "invalid category_id"}), 400

    pid = db.add_product(
        name=name,
        brand=(body.get("brand") or "").strip(),
        category_id=category_id,
        description=(body.get("description") or "").strip(),
        image_url=(body.get("image_url") or "").strip(),
    )
    return jsonify({"id": pid, "message": "Product created"}), 201


@app.route("/api/admin/products/<int:pid>", methods=["PUT"])
def admin_update_product(pid):
    body = request.get_json(force=True)
    name = (body.get("name") or "").strip()
    if not name:
        return jsonify({"error": "name is required"}), 400
    try:
        category_id = int(body.get("category_id", 1))
    except (ValueError, TypeError):
        return jsonify({"error": "invalid category_id"}), 400

    db.update_product(
        pid=pid,
        name=name,
        brand=(body.get("brand") or "").strip(),
        category_id=category_id,
        description=(body.get("description") or "").strip(),
        image_url=(body.get("image_url") or "").strip(),
    )
    return jsonify({"message": "Product updated"})


@app.route("/api/admin/products/<int:pid>", methods=["DELETE"])
def admin_delete_product(pid):
    db.delete_product(pid)
    return jsonify({"message": "Product deleted"})


# ── Admin API — Prices ────────────────────────────────────────────────────────
@app.route("/api/admin/prices", methods=["POST"])
def admin_upsert_price():
    body = request.get_json(force=True)
    platform = body.get("platform", "")
    if platform not in ("GeM", "Amazon", "Flipkart"):
        return jsonify({"error": "platform must be GeM, Amazon, or Flipkart"}), 400
    try:
        product_id = int(body["product_id"])
        price = float(body["price"])
        if price <= 0:
            raise ValueError
    except (KeyError, ValueError, TypeError):
        return jsonify({"error": "valid product_id and price required"}), 400

    collected = (body.get("collected_date") or "").strip() or date.today().isoformat()
    db.upsert_price(
        product_id=product_id,
        platform=platform,
        price=price,
        url=(body.get("url") or "").strip(),
        notes=(body.get("notes") or "").strip(),
        collected_date=collected,
    )
    return jsonify({"message": "Price saved"}), 201


@app.route("/api/admin/prices/<int:price_id>", methods=["DELETE"])
def admin_delete_price(price_id):
    db.delete_price(price_id)
    return jsonify({"message": "Price deleted"})


# ── Admin API — Categories ────────────────────────────────────────────────────
@app.route("/api/admin/categories", methods=["POST"])
def admin_add_category():
    body = request.get_json(force=True)
    name = (body.get("name") or "").strip()
    if not name:
        return jsonify({"error": "name required"}), 400
    try:
        cid = db.add_category(name)
        return jsonify({"id": cid, "name": name}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 409


# ── Health ────────────────────────────────────────────────────────────────────
@app.route("/api/health")
def health():
    return jsonify({"status": "ok", "service": "GeM Price Comparison"})


if __name__ == "__main__":
    import os
    os.makedirs("static", exist_ok=True)

    print("Starting GeM Compare...")
    print("Main site  → http://localhost:8000")
    print("Admin panel→ http://localhost:8000/admin")

    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

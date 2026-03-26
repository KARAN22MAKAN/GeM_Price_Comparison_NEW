import sqlite3
from datetime import date
from pathlib import Path

DB_PATH = Path("gem_compare.db")


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_conn()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS categories (
            id   INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        );

        CREATE TABLE IF NOT EXISTS products (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            name        TEXT NOT NULL,
            brand       TEXT DEFAULT '',
            category_id INTEGER REFERENCES categories(id),
            description TEXT DEFAULT '',
            image_url   TEXT DEFAULT '',
            created_at  TEXT DEFAULT (date('now'))
        );

        CREATE TABLE IF NOT EXISTS price_entries (
            id             INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id     INTEGER NOT NULL REFERENCES products(id) ON DELETE CASCADE,
            platform       TEXT NOT NULL CHECK(platform IN ('GeM','Amazon','Flipkart')),
            price          REAL NOT NULL,
            url            TEXT DEFAULT '',
            collected_date TEXT DEFAULT (date('now')),
            notes          TEXT DEFAULT ''
        );

        CREATE INDEX IF NOT EXISTS idx_price_product  ON price_entries(product_id);
        CREATE INDEX IF NOT EXISTS idx_price_platform ON price_entries(platform);
    """)
    conn.commit()
    conn.close()


# ── Seed data ──────────────────────────────────────────────────────────────────
SEED_DATA = [
    # (category, name, brand, description, image_url, [(platform, price, url, notes)])
    ("Office Supplies", "Ball Point Pen (Pack of 10)", "Cello",
     "Blue ink ball point pens, smooth writing",
     "https://m.media-amazon.com/images/I/71z5nHpqxSL._SL1500_.jpg",
     [("GeM", 45.00, "https://mkp.gem.gov.in", "GST inclusive"),
      ("Amazon", 59.00, "https://amazon.in", "Prime eligible"),
      ("Flipkart", 52.00, "https://flipkart.com", "Assured product")]),

    ("Office Supplies", "A4 Printing Paper (500 Sheets)", "JK Copier",
     "75 GSM copier paper, ream of 500",
     "https://m.media-amazon.com/images/I/81QYHdShe3L._SL1500_.jpg",
     [("GeM", 285.00, "https://mkp.gem.gov.in", "Bulk rate"),
      ("Amazon", 349.00, "https://amazon.in", ""),
      ("Flipkart", 329.00, "https://flipkart.com", "")]),

    ("Office Supplies", "Stapler with 1000 Staples", "Kangaro",
     "Heavy duty stapler, 24/6 staples",
     "https://m.media-amazon.com/images/I/61z+e1PCQPL._SL1200_.jpg",
     [("GeM", 180.00, "https://mkp.gem.gov.in", ""),
      ("Amazon", 229.00, "https://amazon.in", ""),
      ("Flipkart", 199.00, "https://flipkart.com", "")]),

    ("Office Supplies", "Sticky Notes 3x3 (12 Pads)", "3M Post-it",
     "Canary yellow, 100 sheets per pad",
     "https://m.media-amazon.com/images/I/81jmGP0RCHL._SL1500_.jpg",
     [("GeM", 420.00, "https://mkp.gem.gov.in", "Government bulk rate"),
      ("Amazon", 549.00, "https://amazon.in", "Prime"),
      ("Flipkart", 510.00, "https://flipkart.com", "")]),

    ("Electronics", "USB Pen Drive 32GB", "SanDisk",
     "USB 3.0, read speed up to 100MB/s",
     "https://m.media-amazon.com/images/I/61Os9WjCvPL._SL1500_.jpg",
     [("GeM", 399.00, "https://mkp.gem.gov.in", ""),
      ("Amazon", 499.00, "https://amazon.in", "Prime eligible"),
      ("Flipkart", 459.00, "https://flipkart.com", "")]),

    ("Electronics", "USB Pen Drive 64GB", "Kingston",
     "USB 3.2, DataTraveler series",
     "https://m.media-amazon.com/images/I/71WSlWxJxfL._SL1500_.jpg",
     [("GeM", 649.00, "https://mkp.gem.gov.in", ""),
      ("Amazon", 799.00, "https://amazon.in", ""),
      ("Flipkart", 729.00, "https://flipkart.com", "SuperCoin eligible")]),

    ("Electronics", "Webcam HD 1080p", "Logitech",
     "Full HD webcam with built-in mic, plug and play",
     "https://m.media-amazon.com/images/I/61APFpxKRiL._SL1200_.jpg",
     [("GeM", 1850.00, "https://mkp.gem.gov.in", "GeM verified seller"),
      ("Amazon", 2299.00, "https://amazon.in", "Amazon Choice"),
      ("Flipkart", 2149.00, "https://flipkart.com", "")]),

    ("Electronics", "Wireless Mouse", "HP",
     "Optical wireless mouse, 2.4GHz, 3 buttons",
     "https://m.media-amazon.com/images/I/51DUO-GnGhL._SL1200_.jpg",
     [("GeM", 549.00, "https://mkp.gem.gov.in", ""),
      ("Amazon", 699.00, "https://amazon.in", ""),
      ("Flipkart", 649.00, "https://flipkart.com", "")]),

    ("Electronics", "Mechanical Keyboard", "TVS Gold",
     "PS/2 & USB, gold plated contacts",
     "https://m.media-amazon.com/images/I/71LQgVPbhEL._SL1500_.jpg",
     [("GeM", 1299.00, "https://mkp.gem.gov.in", "Popular in govt offices"),
      ("Amazon", 1599.00, "https://amazon.in", ""),
      ("Flipkart", 1499.00, "https://flipkart.com", "")]),

    ("Electronics", "External Hard Disk 1TB", "Seagate",
     "Backup Plus Slim, USB 3.0",
     "https://m.media-amazon.com/images/I/61TpvnVKBiL._SL1500_.jpg",
     [("GeM", 3299.00, "https://mkp.gem.gov.in", ""),
      ("Amazon", 3999.00, "https://amazon.in", "Prime eligible"),
      ("Flipkart", 3749.00, "https://flipkart.com", "")]),

    ("Laptops", "HP Laptop 15s (Core i3, 8GB, 512GB SSD)", "HP",
     "15.6 inch FHD, Windows 11, Intel Core i3 12th Gen",
     "https://m.media-amazon.com/images/I/71eJSmBrxRL._SL1500_.jpg",
     [("GeM", 38999.00, "https://mkp.gem.gov.in", "Government quota pricing"),
      ("Amazon", 44990.00, "https://amazon.in", ""),
      ("Flipkart", 42999.00, "https://flipkart.com", "")]),

    ("Laptops", "Dell Inspiron 15 (Core i5, 16GB, 512GB SSD)", "Dell",
     "15.6 inch FHD, Windows 11, Intel Core i5 12th Gen",
     "https://m.media-amazon.com/images/I/81+qxNJN5iL._SL1500_.jpg",
     [("GeM", 54999.00, "https://mkp.gem.gov.in", "DGS&D rate contract"),
      ("Amazon", 62990.00, "https://amazon.in", ""),
      ("Flipkart", 59999.00, "https://flipkart.com", "Big Billion Day price")]),

    ("Laptops", "Lenovo IdeaPad Slim 3 (Ryzen 5, 8GB, 512GB)", "Lenovo",
     "15.6 inch FHD IPS, AMD Ryzen 5 7520U",
     "https://m.media-amazon.com/images/I/71Ax7AMdYjL._SL1500_.jpg",
     [("GeM", 41500.00, "https://mkp.gem.gov.in", ""),
      ("Amazon", 46990.00, "https://amazon.in", "Prime Day price"),
      ("Flipkart", 44499.00, "https://flipkart.com", "")]),

    ("Printers", "HP LaserJet MFP M141w (Wi-Fi, Print/Scan/Copy)", "HP",
     "Wireless mono laser all-in-one, 20ppm",
     "https://m.media-amazon.com/images/I/61+I4LPNUKL._SL1500_.jpg",
     [("GeM", 11500.00, "https://mkp.gem.gov.in", "Rate contract model"),
      ("Amazon", 13499.00, "https://amazon.in", ""),
      ("Flipkart", 12799.00, "https://flipkart.com", "")]),

    ("Printers", "Canon PIXMA G3010 All-in-One Ink Tank", "Canon",
     "Colour inkjet, Wi-Fi, print/copy/scan, high yield",
     "https://m.media-amazon.com/images/I/51yk+WxLYaL._SL1200_.jpg",
     [("GeM", 10200.00, "https://mkp.gem.gov.in", ""),
      ("Amazon", 12499.00, "https://amazon.in", "Amazon Choice"),
      ("Flipkart", 11799.00, "https://flipkart.com", "")]),

    ("Printers", "Epson L3250 Wi-Fi All-in-One Ink Tank Printer", "Epson",
     "Colour MFP, Wi-Fi Direct, 10ppm black",
     "https://m.media-amazon.com/images/I/61hcNzBKZoL._SL1500_.jpg",
     [("GeM", 11800.00, "https://mkp.gem.gov.in", ""),
      ("Amazon", 13500.00, "https://amazon.in", ""),
      ("Flipkart", 12999.00, "https://flipkart.com", "Flipkart assured")]),

    ("Furniture", "Ergonomic Office Chair with Lumbar Support", "Green Soul",
     "Mesh back, adjustable armrests, 360 swivel",
     "https://m.media-amazon.com/images/I/71GdRGi2E3L._SL1500_.jpg",
     [("GeM", 5499.00, "https://mkp.gem.gov.in", "MSME vendor"),
      ("Amazon", 7499.00, "https://amazon.in", ""),
      ("Flipkart", 6799.00, "https://flipkart.com", "")]),

    ("Furniture", "Wooden Office Table (120x60 cm)", "Nilkamal",
     "Engineered wood, single drawer, walnut finish",
     "https://m.media-amazon.com/images/I/61r4gxTjZ1L._SL1500_.jpg",
     [("GeM", 5200.00, "https://mkp.gem.gov.in", ""),
      ("Amazon", 6999.00, "https://amazon.in", ""),
      ("Flipkart", 6499.00, "https://flipkart.com", "")]),

    ("Furniture", "Steel Almirah (2-Door, 4 Shelves)", "Godrej",
     "Powder coated, 195cm tall, rust proof",
     "https://m.media-amazon.com/images/I/61wCHOjmVEL._SL1500_.jpg",
     [("GeM", 8999.00, "https://mkp.gem.gov.in", "GeM OEM rate"),
      ("Amazon", 10999.00, "https://amazon.in", ""),
      ("Flipkart", 10499.00, "https://flipkart.com", "")]),

    ("Cleaning & Sanitation", "Hand Sanitizer 500ml (Pack of 6)", "Dettol",
     "70% alcohol, instant sanitizer, kills 99.9% germs",
     "https://m.media-amazon.com/images/I/71CypMj3UGL._SL1500_.jpg",
     [("GeM", 480.00, "https://mkp.gem.gov.in", "Government bulk rate"),
      ("Amazon", 599.00, "https://amazon.in", "Subscribe & Save"),
      ("Flipkart", 549.00, "https://flipkart.com", "")]),

    ("Cleaning & Sanitation", "N95 Face Masks (Pack of 50)", "3M",
     "FFP2 rated, BIS approved, adjustable nose clip",
     "https://m.media-amazon.com/images/I/61sCWUz3mJL._SL1200_.jpg",
     [("GeM", 799.00, "https://mkp.gem.gov.in", "BIS certified stock"),
      ("Amazon", 999.00, "https://amazon.in", ""),
      ("Flipkart", 929.00, "https://flipkart.com", "")]),

    ("Cleaning & Sanitation", "Phenyl Floor Cleaner 5L", "Lizol",
     "Disinfectant floor cleaner, citrus fragrance",
     "https://m.media-amazon.com/images/I/71z6LiJqd3L._SL1500_.jpg",
     [("GeM", 349.00, "https://mkp.gem.gov.in", ""),
      ("Amazon", 429.00, "https://amazon.in", ""),
      ("Flipkart", 399.00, "https://flipkart.com", "")]),
]


def seed_db():
    conn = get_conn()
    existing = conn.execute("SELECT COUNT(*) FROM products").fetchone()[0]
    if existing > 0:
        conn.close()
        return

    today = date.today().isoformat()
    for cat_name, prod_name, brand, desc, image, prices in SEED_DATA:
        conn.execute("INSERT OR IGNORE INTO categories(name) VALUES(?)", (cat_name,))
        cat_id = conn.execute("SELECT id FROM categories WHERE name=?", (cat_name,)).fetchone()[0]
        conn.execute(
            "INSERT INTO products(name, brand, category_id, description, image_url) VALUES(?,?,?,?,?)",
            (prod_name, brand, cat_id, desc, image)
        )
        prod_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
        for platform, price, url, notes in prices:
            conn.execute(
                "INSERT INTO price_entries(product_id, platform, price, url, collected_date, notes) VALUES(?,?,?,?,?,?)",
                (prod_id, platform, price, url, today, notes)
            )

    conn.commit()
    conn.close()
    print(f"Seeded {len(SEED_DATA)} products.")


# ── Queries ────────────────────────────────────────────────────────────────────

def row_to_dict(row):
    return dict(row) if row else None


def search_products(query):
    conn = get_conn()
    like = f"%{query}%"
    rows = conn.execute("""
        SELECT p.id, p.name, p.brand, p.description, p.image_url,
               p.category_id, c.name AS category
        FROM products p
        LEFT JOIN categories c ON p.category_id = c.id
        WHERE p.name LIKE ? OR p.brand LIKE ? OR c.name LIKE ? OR p.description LIKE ?
        LIMIT 30
    """, (like, like, like, like)).fetchall()

    results = []
    for row in rows:
        pid = row["id"]
        prices = conn.execute("""
            SELECT id, platform, price, url, collected_date, notes
            FROM price_entries WHERE product_id=? ORDER BY price ASC
        """, (pid,)).fetchall()
        price_list = [dict(p) for p in prices]
        cheapest = price_list[0] if price_list else None
        results.append({
            "id": pid,
            "name": row["name"],
            "brand": row["brand"] or "",
            "category": row["category"] or "",
            "category_id": row["category_id"],
            "description": row["description"] or "",
            "image_url": row["image_url"] or "",
            "prices": price_list,
            "cheapest": cheapest,
        })
    conn.close()
    return results


def get_all_products():
    conn = get_conn()
    rows = conn.execute("""
        SELECT p.id, p.name, p.brand, p.description, p.image_url,
               p.category_id, c.name AS category, p.created_at
        FROM products p
        LEFT JOIN categories c ON p.category_id = c.id
        ORDER BY c.name, p.name
    """).fetchall()

    results = []
    for row in rows:
        pid = row["id"]
        prices = conn.execute(
            "SELECT id, platform, price, url, collected_date, notes FROM price_entries WHERE product_id=? ORDER BY platform",
            (pid,)
        ).fetchall()
        results.append({
            "id": pid,
            "name": row["name"],
            "brand": row["brand"] or "",
            "description": row["description"] or "",
            "image_url": row["image_url"] or "",
            "category": row["category"] or "",
            "category_id": row["category_id"],
            "created_at": row["created_at"],
            "prices": [dict(p) for p in prices],
        })
    conn.close()
    return results


def get_categories():
    conn = get_conn()
    rows = conn.execute("SELECT id, name FROM categories ORDER BY name").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def add_product(name, brand, category_id, description, image_url):
    conn = get_conn()
    conn.execute(
        "INSERT INTO products(name, brand, category_id, description, image_url) VALUES(?,?,?,?,?)",
        (name, brand or "", category_id, description or "", image_url or "")
    )
    pid = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
    conn.commit()
    conn.close()
    return pid


def update_product(pid, name, brand, category_id, description, image_url):
    conn = get_conn()
    conn.execute(
        "UPDATE products SET name=?, brand=?, category_id=?, description=?, image_url=? WHERE id=?",
        (name, brand or "", category_id, description or "", image_url or "", pid)
    )
    conn.commit()
    conn.close()


def delete_product(pid):
    conn = get_conn()
    conn.execute("DELETE FROM products WHERE id=?", (pid,))
    conn.commit()
    conn.close()


def upsert_price(product_id, platform, price, url, notes, collected_date):
    conn = get_conn()
    conn.execute(
        "DELETE FROM price_entries WHERE product_id=? AND platform=?",
        (product_id, platform)
    )
    conn.execute(
        "INSERT INTO price_entries(product_id, platform, price, url, notes, collected_date) VALUES(?,?,?,?,?,?)",
        (product_id, platform, price, url or "", notes or "", collected_date)
    )
    conn.commit()
    conn.close()


def delete_price(price_id):
    conn = get_conn()
    conn.execute("DELETE FROM price_entries WHERE id=?", (price_id,))
    conn.commit()
    conn.close()


def add_category(name):
    conn = get_conn()
    try:
        conn.execute("INSERT INTO categories(name) VALUES(?)", (name,))
        conn.commit()
        cid = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
        conn.close()
        return cid
    except sqlite3.IntegrityError:
        conn.close()
        raise ValueError("Category already exists")


def get_stats():
    conn = get_conn()

    total_products = conn.execute("SELECT COUNT(*) FROM products").fetchone()[0]
    total_prices   = conn.execute("SELECT COUNT(*) FROM price_entries").fetchone()[0]
    total_cats     = conn.execute("SELECT COUNT(*) FROM categories").fetchone()[0]

    win_rows = conn.execute("""
        SELECT pe.platform, COUNT(*) AS wins
        FROM price_entries pe
        WHERE pe.price = (
            SELECT MIN(pe2.price) FROM price_entries pe2 WHERE pe2.product_id = pe.product_id
        )
        GROUP BY pe.platform ORDER BY wins DESC
    """).fetchall()

    avg_rows = conn.execute("""
        SELECT platform, ROUND(AVG(price), 2) AS avg_price
        FROM price_entries GROUP BY platform ORDER BY avg_price ASC
    """).fetchall()

    gem_saving = conn.execute("""
        SELECT ROUND(AVG(comp.min_price - gem.price), 2) AS avg_saving
        FROM price_entries gem
        JOIN (
            SELECT product_id, MIN(price) AS min_price
            FROM price_entries WHERE platform != 'GeM'
            GROUP BY product_id
        ) comp ON gem.product_id = comp.product_id
        WHERE gem.platform = 'GeM'
    """).fetchone()

    conn.close()
    return {
        "total_products": total_products,
        "total_price_entries": total_prices,
        "total_categories": total_cats,
        "platform_wins": [dict(r) for r in win_rows],
        "avg_price_per_platform": [dict(r) for r in avg_rows],
        "avg_gem_saving_vs_others": gem_saving["avg_saving"] if gem_saving and gem_saving["avg_saving"] else 0,
    }

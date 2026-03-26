# GeM Compare — Full Stack Price Comparison App

Compare product prices across GeM, Amazon India, and Flipkart using a verified SQLite database.

**Authors:** Karan Makan, Saransh Agnihotri, Rahul Joshi
**Institution:** Thakur College of Engineering & Technology, Mumbai

---

## Setup & Run (2 steps)

### 1. Install dependency
```bash
pip install Flask
```

### 2. Run
```bash
python app.py
```

Open → http://localhost:8000
Admin → http://localhost:8000/admin

The SQLite database is created and seeded automatically on first run.
No other setup needed.

---

## Files

| File | Purpose |
|------|---------|
| `app.py` | Flask backend — all API routes |
| `database.py` | SQLite schema, seeding, all DB functions |
| `static/index.html` | Main frontend — search + price comparison |
| `static/admin.html` | Admin panel — manage products & prices |

---

## Pre-seeded Data

22 products across 6 categories (66 price entries total):
- Office Supplies, Electronics, Laptops, Printers, Furniture, Cleaning & Sanitation

Key finding from seed data:
- **GeM wins cheapest price on all 22 products**
- Average GeM saving vs competitors: ₹990.59
- Avg GeM price: ₹9,059 | Amazon: ₹10,594 | Flipkart: ₹10,049

---

## API Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/search?q=<query>` | Search + compare prices |
| GET | `/api/stats` | Platform statistics |
| GET | `/api/categories` | List all categories |
| GET | `/api/admin/products` | All products with prices |
| POST | `/api/admin/products` | Add product |
| PUT | `/api/admin/products/<id>` | Update product |
| DELETE | `/api/admin/products/<id>` | Delete product (cascades) |
| POST | `/api/admin/prices` | Add/replace a price entry |
| DELETE | `/api/admin/prices/<id>` | Delete price entry |
| POST | `/api/admin/categories` | Add category |

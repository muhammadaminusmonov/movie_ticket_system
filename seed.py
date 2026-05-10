"""
seed.py — Bootstrap the database for JMeter testing.

Creates:
  - 1 Admin user
  - 1 Cinema Owner user
  - 1 Customer user  (add more below for concurrency tests)
  - 1 Cinema, 1 Screen, 10 Seats
  - 1 Movie, 1 Show

Run inside Docker:
  docker-compose exec backend python seed.py

Run locally (needs DB reachable):
  DATABASE_URL=postgresql://postgres:postgres@localhost:5433/movie_db python seed.py
"""

import os
import sys
from datetime import datetime, timedelta

from dotenv import load_dotenv

load_dotenv()

# ── Validate env ──────────────────────────────────────────────────────────────
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    sys.exit("ERROR: DATABASE_URL not set. Check your .env file.")

# ── DB setup ──────────────────────────────────────────────────────────────────
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

# Import all domain models so Base.metadata knows every table
import app.domain  # noqa: F401
from app.core.database import Base
from app.core.security import hash_password

from app.domain.user import User, UserRole
from app.domain.cinema import Cinema
from app.domain.screen import Screen
from app.domain.seat import Seat, SeatType
from app.domain.movie import Movie
from app.domain.show import Show

# Create all tables (safe to run multiple times — skips existing tables)
Base.metadata.create_all(bind=engine)

db = SessionLocal()


def already_exists(email: str) -> bool:
    return db.query(User).filter_by(email=email).first() is not None


# ── Users ─────────────────────────────────────────────────────────────────────
print("\n[1/5] Creating users...")

if already_exists("admin@cinema.com"):
    print("  ⚠  admin@cinema.com already exists — skipping user creation")
    admin   = db.query(User).filter_by(email="admin@cinema.com").first()
    owner   = db.query(User).filter_by(email="owner@cinema.com").first()
    customer = db.query(User).filter_by(email="customer@cinema.com").first()
else:
    admin = User(
        name="Admin",
        email="admin@cinema.com",
        password_hash=hash_password("admin123"),
        role=UserRole.ADMIN,
    )
    owner = User(
        name="Cinema Owner",
        email="owner@cinema.com",
        password_hash=hash_password("owner123"),
        role=UserRole.OWNER,
    )
    customer = User(
        name="Test Customer",
        email="customer@cinema.com",
        password_hash=hash_password("customer123"),
        role=UserRole.CUSTOMER,
    )
    db.add_all([admin, owner, customer])
    db.commit()
    print("  ✓  admin, owner, customer created")

# ── Cinema ────────────────────────────────────────────────────────────────────
print("\n[2/5] Creating cinema and screen...")

cinema = db.query(Cinema).filter_by(name="Grand Cinema").first()
if not cinema:
    cinema = Cinema(name="Grand Cinema", location="Tashkent", owner_id=owner.id)
    db.add(cinema)
    db.commit()
    print(f"  ✓  Cinema: {cinema.name}")
else:
    print(f"  ⚠  Cinema already exists — skipping")

screen = db.query(Screen).filter_by(cinema_id=cinema.id).first()
if not screen:
    screen = Screen(name="Screen 1", cinema_id=cinema.id)
    db.add(screen)
    db.commit()
    print(f"  ✓  Screen: {screen.name}")
else:
    print(f"  ⚠  Screen already exists — skipping")

# ── Seats (2 rows × 5 seats = 10 total) ──────────────────────────────────────
print("\n[3/5] Creating seats...")

existing_seats = db.query(Seat).filter_by(screen_id=screen.id).all()
if existing_seats:
    seats = existing_seats
    print(f"  ⚠  {len(seats)} seats already exist — skipping")
else:
    seats = []
    for row in ["A", "B"]:
        for number in range(1, 6):
            seat_type = SeatType.VIP if row == "A" else SeatType.STANDARD
            seat = Seat(screen_id=screen.id, row=row, number=number, type=seat_type)
            seats.append(seat)
            db.add(seat)
    db.commit()
    print(f"  ✓  {len(seats)} seats: rows A (VIP) and B (STANDARD)")

# ── Movie ─────────────────────────────────────────────────────────────────────
print("\n[4/5] Creating movie...")

movie = db.query(Movie).filter_by(title="Inception").first()
if not movie:
    movie = Movie(title="Inception", duration_minutes=148)
    db.add(movie)
    db.commit()
    print(f"  ✓  Movie: {movie.title}")
else:
    print(f"  ⚠  Movie already exists — skipping")

# ── Show (tomorrow 19:00 UTC) ─────────────────────────────────────────────────
print("\n[5/5] Creating show...")

tomorrow = (datetime.utcnow() + timedelta(days=1)).replace(
    hour=19, minute=0, second=0, microsecond=0
)
existing_show = db.query(Show).filter_by(movie_id=movie.id, screen_id=screen.id).first()
if existing_show:
    show = existing_show
    print(f"  ⚠  Show already exists — skipping")
else:
    show = Show(
        movie_id=movie.id,
        screen_id=screen.id,
        start_time=tomorrow,
        end_time=tomorrow + timedelta(hours=3),
        price=25000,  # 25,000 UZS per seat
    )
    db.add(show)
    db.commit()
    print(f"  ✓  Show: {show.start_time} UTC, price 25,000 UZS")

db.close()

# ── Summary ───────────────────────────────────────────────────────────────────
print("\n" + "=" * 58)
print("  SEED COMPLETE — copy these into JMeter")
print("=" * 58)

print("\n── Users ───────────────────────────────────────────────")
print(f"  Admin    │ admin@cinema.com    │ admin123")
print(f"  Owner    │ owner@cinema.com    │ owner123")
print(f"  Customer │ customer@cinema.com │ customer123")

print("\n── IDs (paste into JMeter variables) ──────────────────")
print(f"  show_id    = {show.id}")
print(f"  screen_id  = {screen.id}")
print(f"  movie_id   = {movie.id}")
print(f"  cinema_id  = {cinema.id}")

print("\n── Seats ───────────────────────────────────────────────")
for s in seats:
    tag = "VIP     " if s.type == SeatType.VIP else "STANDARD"
    print(f"  {tag} │ row {s.row} seat {s.number} │ {s.id}")

print("\n── JMeter booking flow ─────────────────────────────────")
print("  1. POST /auth/login          → extract token")
print("  2. GET  /shows/${show_id}/seats  → verify availability")
print("  3. POST /cart/add            → body: seat_id, show_id=show_id, price=25000")
print("  4. POST /booking/checkout    → creates PENDING booking")
print("  5. POST /payment/pay         → body: booking_id, amount, method")
print("  6. GET  /bookings/history    → assert status=CONFIRMED")
print("=" * 58 + "\n")
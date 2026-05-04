from fastapi import FastAPI

# Import all domain models so Base.metadata knows every table before create_all()
import app.domain  # noqa: F401

from app.core.database import engine, Base
from app.api import auth, movie, show, cinema, screen, seat, cart, booking, payment

app = FastAPI(
    title="Movie Ticket System",
    description="Backend API — Movie Ticket Booking Platform",
    version="1.0.0",
)


@app.on_event("startup")
def create_tables():
    Base.metadata.create_all(bind=engine)


@app.get("/", tags=["Health"])
def root():
    return {"status": "ok", "message": "Movie Ticket System running"}


# ── Public ───────────────────────────────────────────────────────────────────
app.include_router(auth.router,    prefix="/auth",    tags=["Auth"])
app.include_router(movie.router,   prefix="/movies",  tags=["Movies"])
app.include_router(show.router,    prefix="/shows",   tags=["Shows"])
app.include_router(cinema.router,  prefix="/cinemas", tags=["Cinemas"])

# ── Owner ────────────────────────────────────────────────────────────────────
app.include_router(screen.router,  prefix="/screens", tags=["Screens & Seats"])

# ── Customer booking flow ─────────────────────────────────────────────────────
app.include_router(seat.router,    prefix="/seat",    tags=["Seat Locks"])
app.include_router(cart.router,    prefix="/cart",    tags=["Cart"])
app.include_router(booking.router, prefix="/booking", tags=["Booking"])
app.include_router(payment.router, prefix="/payment", tags=["Payment"])
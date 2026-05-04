# 🎬 Movie Ticket Booking System

A scalable backend system for managing movie ticket bookings, built with **FastAPI**, **PostgreSQL**, and **Redis**.
This project follows a clean, modular architecture designed for real-world production scenarios.

---

## 🚀 Features

* 🔐 Authentication & Authorization (JWT-based)
* 🎥 Movie management
* 🏢 Cinema & screen management
* 🎟️ Seat selection & booking system
* 🛒 Cart system for ticket reservations
* 💳 Payment handling
* 📅 Show scheduling
* ⚡ Redis integration for caching / performance
* 🐳 Dockerized environment for easy deployment

---

## 🧠 Architecture Overview

The project follows a **layered architecture**:

```
app/
├── api/            # Route handlers (controllers)
├── core/           # Core configs (DB, security, dependencies)
├── repositories/   # Data access layer (business logic)
├── main.py         # Entry point
```

### Key Design Decisions

* **Repository Pattern** → separates business logic from API layer
* **Dependency Injection** → clean and testable endpoints
* **Modular APIs** → each domain has its own route module
* **Docker-first setup** → consistent environments

---

## 🛠️ Tech Stack

* **Backend:** FastAPI
* **Database:** PostgreSQL
* **Cache:** Redis
* **Containerization:** Docker & Docker Compose
* **ORM / DB Layer:** SQLAlchemy (assumed from structure)

---

## ⚙️ Setup & Installation

### 1. Clone the repository

```bash
git clone https://github.com/muhammadaminusmonov/movie_ticket_system.git
cd movie_ticket_system
```

---

### 2. Create environment file

```bash
cp .env.example .env
```

Update environment variables as needed.

---

### 3. Run with Docker

```bash
docker-compose up --build
```

---

### 4. Access the API

* API: http://localhost:8000
* Docs (Swagger): http://localhost:8000/docs

---

## 📌 Core Modules

| Module  | Description               |
| ------- | ------------------------- |
| Auth    | User registration & login |
| Movie   | Movie management          |
| Cinema  | Cinema & screens          |
| Show    | Movie show scheduling     |
| Seat    | Seat management           |
| Cart    | Temporary booking storage |
| Booking | Final ticket booking      |
| Payment | Payment processing        |

---

## 🔄 Booking Flow

1. User registers / logs in
2. Browses movies and shows
3. Selects seats
4. Adds tickets to cart
5. Proceeds to payment
6. Booking is confirmed

---

## 🧪 Future Improvements

* Add unit & integration tests
* Implement async DB operations fully
* Add role-based access (admin / user)
* Integrate real payment gateway
* Add notifications (email/SMS)

---

## 📦 Deployment

The project is Dockerized and can be deployed to:

* AWS EC2
* DigitalOcean
* Any container-based hosting

---

## 🤝 Contributing

Contributions are welcome.
Feel free to fork the repo and submit a pull request.

---

## 📄 License

This project is open-source and available under the MIT License.

---

## ⚡ Final Note

This project is a strong foundation for building a **production-ready ticket booking system**.
With proper scaling (load balancing, microservices, etc.), it can evolve into a real-world SaaS platform.

# BookIt API

A booking management system built with **FastAPI**, **SQLAlchemy**, and **PostgreSQL**.


## Features

- Users can browse services, make bookings, and leave reviews.
- Admins can manage users, services, and bookings.
- Secure JWT-based authentication.
- Automatic API docs (`/docs`, `/redoc`).

## Tech Stack

- **FastAPI**: Modern, fast web framework for building APIs
- **SQLAlchemy**: SQL toolkit and Object-Relational Mapping (ORM)
- **PostgreSQL**: Advanced open source relational database
- **Pydantic**: Data validation using Python type annotations
- **JWT**: JSON Web Tokens for secure authentication
- **Alembic**: Database migration tool

## API Endpoints

### Authentication

- `POST /auth/register` Register user
- `POST /auth/login` Login
- `POST /auth/refresh`
- `POST /auth/logout`

### Users

- `GET /me` (current user profile)
- `PATCH /me` (update user)

### Services (public read, admin manage)

- `GET /services` (query: q, price_min, price_max, active)
- `GET /services/{id}`
- `POST /services` (admin)
- `PATCH /services/{id}` (admin)
- `DELETE /services/{id}` (admin)


### Bookings

- `POST /bookings (user creates)`; validate overlaps/conflicts
- `GET /bookings (user: only theirs)`; (admin: all, with filters status, from, to)
- `GET /bookings/{id} (owner or admin)`
- `PATCH /bookings/{id}` (owner can reschedule/cancel if pending or confirmed; admin can update status)
- `DELETE /bookings/{id}` (owner before start_time; admin anytime)


### Reviews

- `POST /reviews` (must be for a completed booking by the same user, one review per booking)
- `GET /services/{id}/reviews`
- `PATCH /reviews/{id}` (owner)
- `DELETE /reviews/{id}` (owner or admin)

##  Setup & Installation

### 1. **Clone Repo**
```bash
git clone https://github.com/muhdfawwazbashir/bookit_api.git
cd Bookit api
```
### 2. **Create virtual environment**
```python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
```
### 3. **Install dependencies**
```bash
   pip install -r requirements.txt
```
### 4. **Environment Setup**
Create a `.env` file with the following variables:
```env
   # Database
   DATABASE_URL=postgresql://username:password@localhost/bookit_api
   
   # JWT
   SECRET_KEY=my-secret-key
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   
   # Email Configuration
   SMTP_HOST=smtp.gmail.com
   SMTP_PORT=587
   SMTP_USER=your-email@gmail.com
   SMTP_PASSWORD=my-app-password
   SMTP_FROM=your-email@gmail.com
   SMTP_FROM_NAME=ClockKo
   
   # OTP Settings
   OTP_EXPIRE_MINUTES=5
```
### 5. **Database setup**
```bash
   # Run migrations
   alembic upgrade head
```
### 6. **Run the application**
```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
```
### API Documentation
Once running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`


## Security Features

- JWT-based authentication
- Password hashing with bcrypt
- CORS middleware configured
- Input validation with Pydantic
- SQL injection protection with SQLAlchemy ORM

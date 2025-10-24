# Flask Authentication & Banner Management API

## Project Overview

This project is a **Flask-based backend API** implementing a secure authentication system with OTP verification and banner management for admins.

---

## Features

### Authentication

- **Register**: Users can register with email and password. OTP is generated for verification and sent via email.
- **OTP Verification**: Users must verify OTP to complete registration.
- **Login**: Users can login and receive a token (JWT/Bcrypt-based).
- **Profile Setup**: Users can update their profile after registration.

### Banner Management (Admin Only)

- **Create, Update, Delete banners** with authorization.
- **Access Control**: Only admin users can manage banners. Non-admins get "Access Denied".

---

## Security & Implementation Details

- **Password Hashing**: All passwords are hashed using `generate_password_hash`.
- **Token-Based Authentication**: Token encodes user ID, decoded on requests to verify identity.
- **Environment Variables**: Sensitive data (DB credentials, secret keys) stored in `.env`.
- **OTP Generation**: Random 4-digit OTP generated using `random.randint`.
- **Authorization Checks**: Admin-only endpoints protected with token validation.

---

## Tech Stack

- **Backend**: Flask, Python 3.8.0
- **Database**: SQLAlchemy

---

# 🚀 Job Application Tracker API

## 📌 Description
A backend API built using FastAPI and PostgreSQL to manage job applications.  
It supports secure authentication, role-based access control, and full CRUD operations.

---

## 🛠 Tech Stack
- FastAPI
- PostgreSQL
- SQLAlchemy
- JWT Authentication
- Bcrypt (Password Hashing)

---

## 🔥 Features
- 🔐 User Authentication (JWT)
- 👤 Role-Based Access (Admin/User)
- 📌 Create, Read, Update, Delete Jobs
- 🔍 Search & Filter Jobs
- 📊 Sorting (latest / oldest)
- 📄 Pagination (skip & limit)

---

## 🗄️ Database Setup
Update DATABASE_URL in database.py with your PostgreSQL credentials.

---
## 🧪 Example Request

POST /register

{
  "name": "vasanth",
  "email": "vasanth@gmail.com",
  "password": "1234"
}

---
## 📂 Project Structure

job-tracker/
│── routes/
│── models.py
│── schemas.py
│── database.py
│── main.py

---

## ⚙️ How to Run

```bash
pip install -r requirements.txt
uvicorn main:app --reload

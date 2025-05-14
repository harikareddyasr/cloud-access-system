# ☁️ Cloud Service Access Management System

This is a backend system developed using **FastAPI** that manages access to cloud services based on user subscription plans. It supports **JWT authentication**, **role-based access (admin vs. user)**, and **API usage tracking**.

---

## 🚀 Features

- 🔐 JWT Authentication and Authorization
- 👥 Role-based access control (Admin/Customer)
- 📦 Subscription Plans with API Access Limits
- 📊 Usage Logging for API Calls
- 🛠️ Admin-only API for Plan Management
- ✅ Interactive Swagger UI at `/docs`

---

## 🛠️ Tech Stack

- **FastAPI** – Web framework
- **SQLite + SQLAlchemy** – Async DB and ORM
- **Pydantic** – Data validation
- **JWT** – Secure token authentication
- **Uvicorn** – ASGI server

---

## 📂 Project Structure

app/
├── crud/
├── database.py
├── main.py
├── models/
├── routes/
├── schemas/
├── utils/
└── cloudaccess.db

## 🧪 How to Run

1. Clone the Project
   ``` git clone https://github.com/yourusername/cloud-access-system.git 
   cd cloud-access-system ```
2. create and activate virtual environment
   ```python3 -m venv env 
   source env/bin/activate  # or on Windows: env\Scripts\activate ```
3. Install dependencies
   ```pip install -r requirements.txt```
4. Run the app
  ``` uvicorn app.main:app --reload```


## 🔐 Authentication Flow

    Register a user (POST /users/)
    Login to get JWT Token (POST /token)
    Authorize via Swagger UI (Click "Authorize" and paste Bearer <token>)

## 📦 Admin Access

    Only role: admin users can:

    View /admin/dashboard
    Manage subscription plans via future endpoints

## 🔄 Sample Endpoints

## Endpoint	                     Method	     Access	        Description
|  /token	                     POST	     Public	        Login and receive JWT token
|  /users/	                     POST	     Public	        Create a user
|  /plans/	                     POST	     Admin	        Create a plan
|  /subscriptions/	             POST	     Authenticated	Subscribe to a plan
|  /cloud/api1 to /cloud/api6	 GET	     Authenticated	API access check + usage

## 📸 Swagger UI

You can interact with all the APIs via http://127.0.0.1:8000/docs

## 📌 Notes

Usage limits for APIs are tracked per user and enforced automatically.
Tokens expire in 30 minutes by default.
You must include Bearer <your_token_here> in headers to access protected routes.

## 🧾 License

This project is for academic use only. You may modify and use it for educational or learning purposes.

👤 Author

Harika Animireddygari
Graduate Student – CSUF
GitHub: https://github.com/harikareddyasr


Cloud Service Access Management System

Overview

This is a backend system built with FastAPI to manage access control for cloud APIs based on user subscriptions. The system supports role-based access control, where admins can define subscription plans, assign permissions, and monitor usage. Customers (users) can subscribe to plans and access services as permitted.

# Features

Role-Based Access Control

Admins can create and manage subscription plans.

Admins can add or update permissions linked to APIs.

Customers can subscribe to plans and access APIs accordingly.

Subscription Plan Management

Create Plan: POST /plans

Update Plan: PUT /plans/{plan_id}

Delete Plan: DELETE /plans/{plan_id}

Permission Management

Add Permission: POST /permissions

Update Permission: PUT /permissions/{permission_id}

Delete Permission: DELETE /permissions/{permission_id}

User Subscription Handling

Subscribe to a Plan: POST /subscriptions

Assign/Modify User Plan (Admin): PUT /subscriptions/{user_id}

Check Current User Usage: GET /usage/limit

Access Control and Usage Tracking
Cloud APIs (Managed Services):

GET /cloud/api1/{user_id}

GET /cloud/api2/{user_id}

GET /cloud/api3/{user_id}

GET /cloud/api4/{user_id}

GET /cloud/api5/{user_id}

GET /cloud/api6/{user_id}

Automatically checks access permissions and usage limits

Tracks number of API calls per user

Denies access if user exceeds their subscription limits

Tech Stack

Python 3.13

FastAPI

SQLite with aiosqlite

SQLAlchemy (Async ORM)

Pydantic

JWT for authentication

Project Structure

app/
├── main.py FastAPI entry point
├── database.py Async DB engine and session
├── models/ SQLAlchemy models
├── schemas/ Pydantic schemas
├── routes/ All API route handlers
├── utils/ Auth and dependencies

Setup Instructions

Clone the Repository
git clone https://github.com/your-username/cloud-access-system.git
cd cloud-access-system

Create Virtual Environment
python3 -m venv venv
source venv/bin/activate

Install Requirements
pip install -r requirements.txt

Run the Application
uvicorn app.main:app --reload

Access API Docs
Visit http://127.0.0.1:8000/docs to explore Swagger UI with full API details

Team Members

Yashwanth Reddy Mallareddygari
Harika Animireddy Gari
snigdha Aravapalli

# Deliverables

All core features implemented

Role-based authentication and authorization

Subscription and permission management

Usage tracking and limit enforcement

REST API with JWT security

Swagger documentation via /docs

Final video walkthrough (included in repo if applicable)

# Notes

All APIs require JWT authentication.

Admin credentials should be seeded manually or registered first with the admin role.
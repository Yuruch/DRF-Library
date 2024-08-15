# DRF-Library  

API service for library management written on DRF

# Features    

- JWT Authentication: Secure user authentication using JSON Web Tokens.  
- Admin Panel: Built-in Django admin for managing books and users.  
- Swagger Documentation: Interactive API documentation using Swagger.  
- CRUD for Books: Create, read, update, and delete operations for managing books.    
- CRUD for Users: User management with email support and JWT authentication.  
- Borrowing Management: Track and manage book borrowings, including overdue notifications.  
- Telegram Notifications: Send notifications via Telegram for borrowing events and overdue books.  
- Scheduled Tasks: Automated tasks for checking overdue borrowings using Django-Celery.  
- Stripe Integration: Payment processing with Stripe for borrowing fees.  
- Dynamic Filters: Filter borrowings and payments based on user and status.  
- Custom Error Handling: Detailed error responses and exception handling.  

# Installing using GitHub 

Install PostgresSQL and create db  

```bash
git clone https://github.com/Yuruch/DRF-Library   
python -m venv venv  
source venv/bin/activate  
pip install -r requirements.txt  
```



# Environment variables

This project is fully relying on environment variables, so you have to create .env file

You can find .env.example in project root


# Run with docker  

```bash
docker compose up  
```

# Run locally

```bash
python manage.py migrate
python manage.py runserver
```
Use the `python manage.py loaddata fixtures.json` 

command to load data from the fixtures.

# Getting access 

**Create user via** /api/user/register/    
**Login via** /api/user/token/  



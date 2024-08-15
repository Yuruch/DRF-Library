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


```bash
python manage.py migrate
python manage.py runserver
```



# Run with docker  

docker compose build  
docker compose up  


# Getting access 

create user via /api/user/register/    
login via /api/user/token/  

Use the `python manage.py loaddata file_name.json` command to load data from the fixtures.
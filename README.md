# Full-Stack Decoupled Architecture: Technical Synopsis

This document provides a comprehensive overview of the design patterns, network routing configurations, resource optimizations, and infrastructure mechanics driving the Employee Management System deployment on AWS EC2 Free Tier.

---

# 🏗️ 1. Architectural Patterns & Decoupling

The application follows a modern decoupled full-stack architecture by separating:

- Frontend delivery
- Backend API processing
- Database execution

This separation improves:
- scalability
- maintainability
- security
- resource efficiency

## High-Level Architecture

```text
                [ Client Browser ]
                        |
                HTTP/HTTPS (80/443)
                        |
                [ Nginx Web Server ]
                 /                \
                /                  \
   Static Frontend Files       Reverse Proxy
      (/var/www/html)                |
                                     |
                              [ FastAPI Service ]
                              (127.0.0.1:5000)
                                     |
                                     |
                              MySQL Protocol
                                 (3306)
                                     |
                              [ MySQL / RDS ]
                              Stored Procedures
```

---

# 🏗️ Phase 1: SSH Into EC2 & Clone Repository

# Step 2.1 — Connect Using SSH

From your local terminal:

```bash
chmod 400 ~/Downloads/my-key.pem
```

Connect:

```bash
ssh -i ~/Downloads/my-key.pem ubuntu@YOUR_EC2_PUBLIC_IP
```

---

# Step 2.2 — Install Git & Clone Repository

Update packages:

```bash
sudo apt update
sudo apt install -y git
```

Clone repository:

```bash
wget https://github.com/pranwagh11/Employee_manegement/archive/refs/heads/main.zip
unzip main.zip
```

---

# Verify Project Structure

```bash
ls -R ~/Employee_manegement
```

Expected structure:

```text
~/Employee_manegement/
├── back/
│   ├── app.py
│   ├── controller.py
│   ├── repository.py
│   ├── schemas.py
│   └── requirements.txt
│
├── front/
│   └── index.html
│
├── setup_backend.sh
├── setup_frontend.sh
└── .env
```

---

# Step 3.1 — Install MySQL Server

Update package indexes and install MySQL server:

```bash
sudo apt update
sudo apt install -y mysql-server
```

---

# Step 3.2 — Start and Enable MySQL Service

```bash
sudo systemctl enable mysql
sudo systemctl start mysql
```

Verify service status:

```bash
sudo systemctl status mysql
```

---

# Step 3.3 — Configure MySQL Root Password

Login to MySQL shell:

```bash
sudo mysql
```

Inside MySQL execute:

```sql
ALTER USER 'root'@'localhost'
IDENTIFIED WITH mysql_native_password
BY 'YourSecurePassword123!';

FLUSH PRIVILEGES;
```

Exit MySQL:

```sql
EXIT;
```

---

# Step 3.4 — Login Using Root Password

Now authenticate using the configured password:

```bash
mysql -u root -p
```

Enter:

```text
YourSecurePassword123!
```

---

# Step 3.5 — Execute Existing Database Schema File

Your project already contains:

```text
DBschema.sql
```


## Option A — Execute Directly From Linux Terminal (Recommended)

Exit MySQL shell if currently inside it:

```sql
EXIT;
```

Then run:

```bash
mysql -u root -p < ~/Employee_manegement/DBschema.sql
```

If your schema file is inside another folder:

```bash
mysql -u root -p < ~/Employee_manegement/back/DBschema.sql
```

Enter your MySQL password when prompted.

---

# Step 3.6 — Verify Database Creation

Login again:

```bash
mysql -u root -p
```

Show databases:

```sql
SHOW DATABASES;
```

Select database:

```sql
USE company_db;
```

Verify tables:

```sql
SHOW TABLES;
```

Verify employee records:

```sql
SELECT * FROM employees;
```

Verify stored procedures:

```sql
SHOW PROCEDURE STATUS
WHERE Db = 'company_db';
```

---

# Expected Result

You should now have:

```text
company_db
└── employees
└── ManageEmployee()
```

fully configured and ready for FastAPI backend integration.

# 🏗️ Phase 4: Configure Environment Variables

---

# Step 4.1 — Create `.env` File

```bash
nano ~/Employee_manegement/.env
```

Paste:

```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=YourSecurePassword123!
DB_DATABASE=company_db

API_PORT=5000

EC2_PUBLIC_IP=YOUR_EC2_PUBLIC_IP
```

Save:
```text
CTRL + O
ENTER
CTRL + X
```

---

# 🏗️ Phase 5: Backend Setup (FastAPI)

---

# Step 5.1 — Create Virtual Environment

```bash
cd ~/Employee_manegement/back

python3 -m venv venv
```

Activate:

```bash
source venv/bin/activate
pip install fastapi uvicorn pymysql python-dotenv
pip install flask flask-cors python-dotenv mysql-connector-python
```

---

# Step 5.2 — Install Python Dependencies

```bash
pip install fastapi uvicorn pymysql python-dotenv
```

Or:

```bash
pip install -r requirements.txt
```

---

# Step 5.3 — Run FastAPI Server

```bash
python app.py
```

---

# Verify API

Open:

```text
http://YOUR_EC2_PUBLIC_IP:5000/docs
```

Swagger UI should appear.

---

# 🏗️ Phase 6: Install and Configure Nginx

---

# Step 6.1 — Install Nginx

```bash
sudo apt install -y nginx
```

Start service:

```bash
sudo systemctl enable nginx
sudo systemctl start nginx
```

---

# Step 6.2 — Deploy Frontend Files

Copy frontend:

```bash
sudo rm -rf /var/www/html/*
```

```bash
sudo cp -r ~/Employee_manegement/front/* /var/www/html/
```

---# 🏗️ Phase 1: SSH Into EC2 & Clone Repository

# Step 2.1 — Connect Using SSH

From your local terminal:

```bash
chmod 400 ~/Downloads/my-key.pem
```

Connect:

```bash
ssh -i ~/Downloads/my-key.pem ubuntu@YOUR_EC2_PUBLIC_IP
```

---

# Step 2.2 — Install Git & Clone Repository

Update packages:

```bash
sudo apt update
sudo apt install -y git
```

Clone repository:

```bash
wget https://github.com/pranwagh11/Employee_manegement/archive/refs/heads/main.zip
unzip main.zip
```

---

# Verify Project Structure

```bash
ls -R ~/Employee_manegement
```

Expected structure:

```text
~/Employee_manegement/
├── back/
│   ├── app.py
│   ├── controller.py
│   ├── repository.py
│   ├── schemas.py
│   └── requirements.txt
│
├── front/
│   └── index.html
│
├── setup_backend.sh
├── setup_frontend.sh
└── .env
```

---

# Step 3.1 — Install MySQL Server

Update package indexes and install MySQL server:

```bash
sudo apt update
sudo apt install -y mysql-server
```

---

# Step 3.2 — Start and Enable MySQL Service

```bash
sudo systemctl enable mysql
sudo systemctl start mysql
```

Verify service status:

```bash
sudo systemctl status mysql
```

---

# Step 3.3 — Configure MySQL Root Password

Login to MySQL shell:

```bash
sudo mysql
```

Inside MySQL execute:

```sql
ALTER USER 'root'@'localhost'
IDENTIFIED WITH mysql_native_password
BY 'YourSecurePassword123!';

FLUSH PRIVILEGES;
```

Exit MySQL:

```sql
EXIT;
```

---

# Step 3.4 — Login Using Root Password

Now authenticate using the configured password:

```bash
mysql -u root -p
```

Enter:

```text
YourSecurePassword123!
```

---

# Step 3.5 — Execute Existing Database Schema File

Your project already contains:

```text
DBschema.sql
```


## Option A — Execute Directly From Linux Terminal (Recommended)

Exit MySQL shell if currently inside it:

```sql
EXIT;
```

Then run:

```bash
mysql -u root -p < ~/Employee_manegement/DBschema.sql
```

If your schema file is inside another folder:

```bash
mysql -u root -p < ~/Employee_manegement/back/DBschema.sql
```

Enter your MySQL password when prompted.

---

# Step 3.6 — Verify Database Creation

Login again:

```bash
mysql -u root -p
```

Show databases:

```sql
SHOW DATABASES;
```

Select database:

```sql
USE company_db;
```

Verify tables:

```sql
SHOW TABLES;
```

Verify employee records:

```sql
SELECT * FROM employees;
```

Verify stored procedures:

```sql
SHOW PROCEDURE STATUS
WHERE Db = 'company_db';
```

---

# Expected Result

You should now have:

```text
company_db
└── employees
└── ManageEmployee()
```

fully configured and ready for FastAPI backend integration.

# 🏗️ Phase 4: Configure Environment Variables

---

# Step 4.1 — Create `.env` File

```bash
nano ~/Employee_manegement/.env
```

Paste:

```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=YourSecurePassword123!
DB_DATABASE=company_db

API_PORT=5000

EC2_PUBLIC_IP=YOUR_EC2_PUBLIC_IP
```

Save:
```text
CTRL + O
ENTER
CTRL + X
```

---

# 🏗️ Phase 5: Backend Setup (FastAPI)

---

# Step 5.1 — Create Virtual Environment

```bash
cd ~/Employee_manegement/back

python3 -m venv venv
```

Activate:

```bash
source venv/bin/activate
pip install fastapi uvicorn pymysql python-dotenv
pip install flask flask-cors python-dotenv mysql-connector-python
```

---

# Step 5.2 — Install Python Dependencies

```bash
pip install fastapi uvicorn pymysql python-dotenv
```

Or:

```bash
pip install -r requirements.txt
```

---

# Step 5.3 — Run FastAPI Server

```bash
python app.py
```

---

# Verify API

Open:

```text
http://YOUR_EC2_PUBLIC_IP:5000/docs
```

Swagger UI should appear.

---

# 🏗️ Phase 6: Install and Configure Nginx

---

# Step 6.1 — Install Nginx

```bash
sudo apt install -y nginx
```

Start service:

```bash
sudo systemctl enable nginx
sudo systemctl start nginx
```

---

# Step 6.2 — Deploy Frontend Files

Copy frontend:

```bash
sudo rm -rf /var/www/html/*
```

```bash
sudo cp -r ~/Employee_manegement/front/* /var/www/html/
```

---

# 🚀 Backend Service Deployment

## Install Dependencies
```
cd /Employee_manegement/back/
python3 -m venv venv
source venv/bin/activate

pip install fastapi uvicorn pymysql python-dotenv
pip install flask flask-cors python-dotenv mysql-connector-python
```



# Configure Security Group

Add inbound rules:

| Type | Port | Source |
|---|---|---|
| HTTP | 80 | 0.0.0.0/0 |
| Custom TCP | 5000 | 0.0.0.0/0 |
| SSH | 22 | Your IP |

---



---

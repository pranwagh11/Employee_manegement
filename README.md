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

# 🌐 2. Frontend Layer

## Frontend Workspace (`/front`)

### Composition
- Static `index.html`
- Vanilla JavaScript
- CSS styling

### Delivery Engine
Served directly through:

- **Nginx**
- Port `80`

### Design Philosophy

Static assets are handled entirely by Nginx instead of Python.

Advantages:
- lower memory consumption
- reduced CPU usage
- kernel-level file streaming
- faster request throughput
- avoids Python template rendering overhead

---

# ⚙️ 3. Backend API Layer

## Backend Workspace (`/back`)

### Technology Stack
- FastAPI
- Uvicorn
- Pydantic
- Repository Pattern
- Controller Layer

### Execution Model

The backend operates purely as a REST API engine.

Responsibilities:
- request validation
- JSON serialization
- business orchestration
- database communication

### Example API Endpoints

```http
GET    /api/employees
POST   /api/employees
PUT    /api/employees/{id}
DELETE /api/employees/{id}
```

---

# 🧱 4. Repository & Controller Pattern

The backend follows layered abstraction:

```text
Client Request
      ↓
FastAPI Route
      ↓
Controller Layer
      ↓
Repository Factory
      ↓
Database Procedure
```

Advantages:
- clean separation of concerns
- reusable business logic
- simplified testing
- database abstraction
- easier future migrations

---

# 🗄️ 5. Database Procedural Isolation

All transactional logic is centralized inside a MySQL Stored Procedure:

```sql
CALL ManageEmployee(...)
```

## Procedure Operation Matrix

| Flag | Operation | Behavior |
|------|-----------|-----------|
| 1 | READ | Returns all employees |
| 2 | CREATE | Inserts new employee |
| 3 | UPDATE | Updates employee |
| 4 | DELETE | Removes employee |

---

## Example Stored Procedure

```sql
DELIMITER $$

CREATE PROCEDURE ManageEmployee(
    IN p_flag INT,
    IN p_id INT,
    IN p_name VARCHAR(100),
    IN p_email VARCHAR(100),
    IN p_position VARCHAR(100),
    IN p_salary DECIMAL(10,2)
)
BEGIN

    IF p_flag = 1 THEN

        SELECT * FROM employees;

    ELSEIF p_flag = 2 THEN

        INSERT INTO employees(name,email,position,salary)
        VALUES(p_name,p_email,p_position,p_salary);

    ELSEIF p_flag = 3 THEN

        UPDATE employees
        SET
            name = p_name,
            email = p_email,
            position = p_position,
            salary = p_salary
        WHERE id = p_id;

    ELSEIF p_flag = 4 THEN

        DELETE FROM employees
        WHERE id = p_id;

    END IF;

END$$

DELIMITER ;
```

---

# 🔒 6. Database Security Advantages

Using parameterized stored procedure calls provides:

- reduced SQL exposure
- centralized transaction logic
- reusable execution plans
- lower query parsing overhead
- mitigation against SQL injection vectors

---

# 📡 7. Network Routing & Binding

## Public Interface Binding

FastAPI/Uvicorn binds using:

```python
host="0.0.0.0"
```

Meaning:
- listen on all network interfaces
- accept external traffic
- expose service publicly

---

## Reverse Proxy Architecture

Nginx handles:
- public traffic
- SSL termination
- static file serving
- reverse proxy forwarding

### Nginx Flow

```text
Browser
   ↓
Nginx (:80 / :443)
   ↓
FastAPI (:5000 localhost only)
```

Advantages:
- backend hidden from internet
- improved security
- centralized traffic management

---

# 🔄 8. CORS Configuration

Frontend and backend operate on different origins.

Example:
- Frontend → Port 80
- API → Port 5000

Therefore CORS must be enabled.

## FastAPI Example

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
```

---

# ☁️ 9. AWS Free Tier Optimization

## EC2 Resource Constraints

AWS Free Tier instances:
- t2.micro
- t3.micro

Provide:
- 1GB RAM

Optimization is essential.

---

# 💾 10. Swap Memory Extension

## Create 2GB Swap File

```bash
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

## Persist Across Reboots

```bash
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
```

Advantages:
- prevents OOM crashes
- stabilizes MySQL
- stabilizes API workers

---

# 🛠️ 11. MySQL Low-Memory Optimization

## Example Configuration

```ini
[mysqld]

innodb_buffer_pool_size = 128M
innodb_log_buffer_size = 8M
max_connections = 20
```

Advantages:
- reduced RAM pressure
- stable operation on Free Tier

---

# 🚀 12. Backend Service Deployment

## Install Dependencies

```bash
python3 -m venv venv
source venv/bin/activate

pip install fastapi uvicorn pymysql python-dotenv
```

---

# ▶️ 13. Running FastAPI

## Development

```bash
uvicorn app:app --host 0.0.0.0 --port 5000
```

## Production

```bash
uvicorn app:app \
  --host 0.0.0.0 \
  --port 5000 \
  --workers 1
```

---

# ⚡ 14. Systemd Service Automation

## Service File

```ini
[Unit]
Description=FastAPI Employee Service
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/Employee_manegement/back
ExecStart=/home/ubuntu/Employee_manegement/back/venv/bin/uvicorn app:app --host 0.0.0.0 --port 5000
Restart=always

[Install]
WantedBy=multi-user.target
```

---

# 🔧 15. Enable Service

```bash
sudo systemctl daemon-reload
sudo systemctl enable fastapi-app
sudo systemctl start fastapi-app
```

---

# 🌍 16. Nginx Reverse Proxy Configuration

## Example Configuration

```nginx
server {

    listen 80;

    server_name _;

    root /var/www/html;

    index index.html;

    location / {
        try_files $uri $uri/ =404;
    }

    location /api/ {

        proxy_pass http://127.0.0.1:5000/;

        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;

    }

}
```

---

# 🔍 17. Infrastructure Diagnostic Commands

## Check Backend Logs

```bash
sudo journalctl -u fastapi-app -f -n 50
```

---

## Verify Network Ports

```bash
sudo netstat -tuln | grep -E '80|5000|3306'
```

---

## Monitor Memory Usage

```bash
free -h -s 3
```

---

## Restart Services

```bash
sudo systemctl restart fastapi-app
sudo systemctl restart nginx
```

---

# 🧠 18. Architectural Benefits Summary

| Layer | Benefit |
|------|----------|
| Nginx | Efficient static delivery |
| FastAPI | High-performance async APIs |
| Repository Pattern | Clean abstraction |
| Stored Procedures | Centralized DB logic |
| Swap Memory | Prevents OOM crashes |
| Reverse Proxy | Security + scalability |
| Systemd | Automatic process recovery |

---

# ✅ Final Production Architecture

```text
                    INTERNET
                        |
                 HTTP / HTTPS
                        |
                    [ NGINX ]
              Static + Reverse Proxy
                        |
              -------------------
              |                 |
      Frontend Assets       /api/*
                                |
                        [ FASTAPI ]
                          Uvicorn
                                |
                          [ MySQL ]
                      Stored Procedures

#TUTORIAL

# 🚀 Step-by-Step Production Deployment Tutorial

This tutorial guides you through deploying a production-ready decoupled full-stack application using:

- **FastAPI** backend
- **Nginx** reverse proxy
- **MySQL** database
- **Stored Procedures**
- **AWS EC2 Free Tier**

The architecture separates frontend delivery from backend API processing for improved scalability, maintainability, and resource efficiency.

---

# 🏗️ Phase 1: Launch and Configure AWS EC2

---

# Step 1.1 — Launch EC2 Instance

1. Log into AWS Console.
2. Navigate to:
   - **EC2 Dashboard**
   - Click **Launch Instance**

---

## Configure Instance

| Setting | Value |
|---|---|
| Name | `employee-management-server` |
| AMI | Ubuntu LTS (Free Tier Eligible) |
| Instance Type | `t2.micro` or `t3.micro` |
| Key Pair | Create/download `.pem` file |

Example key:
```text
my-key.pem
```

---

# Step 1.2 — Configure Security Group

Add inbound rules:

| Type | Port | Source |
|---|---|---|
| HTTP | 80 | 0.0.0.0/0 |
| Custom TCP | 5000 | 0.0.0.0/0 |
| SSH | 22 | Your IP |

---

# 🏗️ Phase 2: SSH Into EC2 & Clone Repository

---

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

# 🏗️ Phase 3: Install and Configure MySQL

---

# 🏗️ Phase 3: Install and Initialize MySQL Database

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

This file includes:
- database creation
- tables
- stored procedures
- initial schema logic

---

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
uvicorn app:app --host 0.0.0.0 --port 5000
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

# Step 6.3 — Configure Reverse Proxy

Edit config:

```bash
sudo nano /etc/nginx/sites-available/default
```

Replace with:

```nginx
server {

    listen 80;

    server_name _;

    root /var/www/html;

    index index.html;

    location / {

        try_files $uri $uri/ =404;

    }

    location /api/ {

        proxy_pass http://127.0.0.1:5000/;

        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;

    }

}
```

---

# Step 6.4 — Restart Nginx

```bash
sudo nginx -t
```

```bash
sudo systemctl restart nginx
```

---

# 🏗️ Phase 7: Production Service Automation

---

# Step 7.1 — Create Systemd Service

```bash
sudo nano /etc/systemd/system/fastapi-app.service
```

Paste:

```ini
[Unit]
Description=FastAPI Employee Service
After=network.target

[Service]

User=ubuntu

WorkingDirectory=/home/ubuntu/Employee_manegement/back

ExecStart=/home/ubuntu/Employee_manegement/back/venv/bin/uvicorn app:app --host 0.0.0.0 --port 5000

Restart=always

[Install]
WantedBy=multi-user.target
```

---

# Step 7.2 — Enable Backend Service

```bash
sudo systemctl daemon-reload
```

```bash
sudo systemctl enable fastapi-app
```

```bash
sudo systemctl start fastapi-app
```

---

# Verify Status

```bash
sudo systemctl status fastapi-app
```

---

# 🏗️ Phase 8: AWS Free Tier Memory Optimization

---

# Step 8.1 — Create Swap Memory

```bash
sudo fallocate -l 2G /swapfile
```

```bash
sudo chmod 600 /swapfile
```

```bash
sudo mkswap /swapfile
```

```bash
sudo swapon /swapfile
```

Persist after reboot:

```bash
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
```

---

# Step 8.2 — Optimize MySQL Memory

Edit config:

```bash
sudo nano /etc/mysql/mysql.conf.d/mysqld.cnf
```

Add:

```ini
[mysqld]

innodb_buffer_pool_size = 128M

innodb_log_buffer_size = 8M

max_connections = 20
```

Restart MySQL:

```bash
sudo systemctl restart mysql
```

---

# 🧪 Phase 9: Final Verification

---

# Verify Frontend

Open browser:

```text
http://YOUR_EC2_PUBLIC_IP
```

---

# Verify API

Open:

```text
http://YOUR_EC2_PUBLIC_IP:5000/docs
```

---

# Verify API JSON

```text
http://YOUR_EC2_PUBLIC_IP:5000/api/employees
```

---

# 🔍 Useful Infrastructure Commands

---

# Backend Logs

```bash
sudo journalctl -u fastapi-app -f -n 50
```

---

# Network Ports

```bash
sudo netstat -tuln | grep -E '80|5000|3306'
```

---

# Memory Monitoring

```bash
free -h -s 3
```

---

# Restart Services

```bash
sudo systemctl restart fastapi-app
```

```bash
sudo systemctl restart nginx
```

```bash
sudo systemctl restart mysql
```

---

# ✅ Final Production Architecture

```text
                    INTERNET
                        |
                 HTTP / HTTPS
                        |
                    [ NGINX ]
              Static + Reverse Proxy
                        |
              -------------------
              |                 |
      Frontend Assets       /api/*
                                |
                        [ FASTAPI ]
                          Uvicorn
                                |
                          [ MySQL ]
                      Stored Procedures
```

---

# 🎯 Final Result

You now have:

- Production-style architecture
- Decoupled frontend/backend
- Reverse proxy routing
- FastAPI async backend
- MySQL stored procedure abstraction
- AWS Free Tier optimized deployment
- Automatic service recovery
- Public API exposure
- Swagger API documentation





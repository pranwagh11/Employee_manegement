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



# 🚀 12. Backend Service Deployment

## Install Dependencies

cd /Employee_manegement/back/
python3 -m venv venv
source venv/bin/activate

pip install fastapi uvicorn pymysql python-dotenv
pip install flask flask-cors python-dotenv mysql-connector-python
```

---

# ▶️ 13. Running FastAPI

## Development

  python app.py
```

## Production

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


# 🚀 Production Deployment Tutorial

This guide walks through deploying a modern decoupled full-stack application on an AWS EC2 Free Tier instance using:

- **FastAPI** for backend API services
- **Nginx** for frontend hosting and reverse proxy routing
- **MySQL** with Stored Procedures for database operations
- **Ubuntu Linux** cloud infrastructure on AWS EC2

The system follows a production-style architecture where:

- the frontend is served independently through Nginx,
- the backend operates as a dedicated REST API service,
- and the database layer is isolated through procedural SQL execution.

This separation improves:

- scalability
- maintainability
- security
- resource optimization
- deployment flexibility

---

# 🏗️ Phase 1 — Launch and Configure AWS EC2

---

# Step 1.1 — Create the EC2 Virtual Machine

1. Sign in to the AWS Management Console.
2. Open the **EC2 Dashboard**.
3. Click:

```text
Launch Instance
```

---

# Configure Instance Parameters

| Configuration | Value |
|---|---|
| Instance Name | `employee-management-server` |
| Operating System | Ubuntu LTS (Free Tier Eligible) |
| Instance Type | `t2.micro` or `t3.micro` |
| Authentication | Create or select an existing Key Pair |

---

# Download SSH Key Pair

AWS generates a secure `.pem` authentication key.

Example:

```text
my-key.pem
```

Important:
- Download it immediately
- Store it securely
- AWS cannot regenerate the same key later

This file is required to remotely access your server using SSH.




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





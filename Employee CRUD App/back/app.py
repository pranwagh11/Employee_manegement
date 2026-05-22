import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

from repository import EmployeeRepositoryFactory
from controller import EmployeeController
from schemas import EmployeeCreate, EmployeeResponse

app = FastAPI(title="Employee Management System API")

# Allow Nginx/Frontend cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER'),       
    'password': os.getenv('DB_PASSWORD', ''),       
    'database': os.getenv('DB_DATABASE')
}

repository_instance = EmployeeRepositoryFactory.get_repository('MYSQL', DB_CONFIG)
controller = EmployeeController(repository_instance)

# ==========================================
# REST API ENDPOINTS
# ==========================================

@app.get("/api/employees", response_model=list[EmployeeResponse])
def get_employees():
    return controller.get_all_employees()

@app.post("/api/employees", status_code=201)
def add_employee(employee: EmployeeCreate):
    return controller.create_employee(employee)

@app.put("/api/employees/{emp_id}")
def edit_employee(emp_id: int, employee: EmployeeCreate):
    return controller.update_employee(emp_id, employee)

@app.delete("/api/employees/{emp_id}")
def remove_employee(emp_id: int):
    return controller.delete_employee(emp_id)


if __name__ == '__main__':
    import uvicorn
    host_ip = os.getenv('HOST_IP', '0.0.0.0')
    port_config = int(os.getenv('API_PORT', 5000)) 
    uvicorn.run("app:app", host=host_ip, port=port_config, reload=False)

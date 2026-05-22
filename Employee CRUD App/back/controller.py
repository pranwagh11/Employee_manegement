from fastapi import HTTPException
import mysql.connector

class EmployeeController:
    def __init__(self, repository):
        self.repository = repository

    def get_all_employees(self):
        try:
            return self.repository.get_all()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Database failure: {str(e)}")

    def create_employee(self, employee_data):
        try:
            new_id = self.repository.create(
                employee_data.name, 
                employee_data.email, 
                employee_data.position, 
                float(employee_data.salary)
            )
            return {"message": "Employee created successfully", "id": new_id}
        except mysql.connector.Error as err:
            raise HTTPException(status_code=400, detail=f"Insertion failed: {str(err)}")

    def update_employee(self, emp_id: int, employee_data):
        try:
            self.repository.update(
                emp_id, 
                employee_data.name, 
                employee_data.email, 
                employee_data.position, 
                float(employee_data.salary)
            )
            return {"message": "Employee updated successfully"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def delete_employee(self, emp_id: int):
        try:
            self.repository.delete(emp_id)
            return {"message": "Employee deleted successfully"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

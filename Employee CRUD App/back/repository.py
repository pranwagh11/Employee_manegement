import mysql.connector
from abc import ABC, abstractmethod

class BaseEmployeeRepository(ABC):
    @abstractmethod
    def get_all(self): pass
    @abstractmethod
    def create(self, name, email, position, salary): pass
    @abstractmethod
    def update(self, emp_id, name, email, position, salary): pass
    @abstractmethod
    def delete(self, emp_id): pass


class MySQLEmployeeRepository(BaseEmployeeRepository):
    def __init__(self, config):
        self.config = config

    def _get_connection(self):
        return mysql.connector.connect(**self.config)

    def get_all(self):
        conn = self._get_connection()
        cursor = conn.cursor(dictionary=True)
        employees = []
        try:
            # Flag 1: SELECT
            cursor.callproc('ManageEmployee', (1, None, None, None, None, None))
            for result in cursor.stored_results():
                employees = result.fetchall()
        finally:
            cursor.close()
            conn.close()
        return employees

    def create(self, name, email, position, salary):
        conn = self._get_connection()
        cursor = conn.cursor(dictionary=True)
        params = (2, None, name, email, position, salary) # Flag 2: INSERT
        new_id = None
        try:
            cursor.callproc('ManageEmployee', params)
            for result in cursor.stored_results():
                row = result.fetchone()
                if row:
                    new_id = row['id']
            conn.commit()
        finally:
            cursor.close()
            conn.close()
        return new_id

    def update(self, emp_id, name, email, position, salary):
        conn = self._get_connection()
        cursor = conn.cursor(dictionary=True)
        params = (3, emp_id, name, email, position, salary) # Flag 3: UPDATE
        try:
            cursor.callproc('ManageEmployee', params)
            conn.commit()
        finally:
            cursor.close()
            conn.close()

    def delete(self, emp_id):
        conn = self._get_connection()
        cursor = conn.cursor(dictionary=True)
        params = (4, emp_id, None, None, None, None) # Flag 4: DELETE
        try:
            cursor.callproc('ManageEmployee', params)
            conn.commit()
        finally:
            cursor.close()
            conn.close()


class EmployeeRepositoryFactory:
    @staticmethod
    def get_repository(repo_type, config):
        if repo_type.upper() == 'MYSQL':
            return MySQLEmployeeRepository(config)
        raise ValueError(f"Unknown repository strategy provider: {repo_type}")

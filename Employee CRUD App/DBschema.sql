CREATE DATABASE IF NOT EXISTS company_db;
USE company_db;

CREATE TABLE IF NOT EXISTS employees (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    position VARCHAR(100) NOT NULL,
    salary DECIMAL(10, 2) NOT NULL
);

use 

DELIMITER $$

CREATE PROCEDURE company_db.ManageEmployee(
    IN p_flag INT,
    IN p_id INT,
    IN p_name VARCHAR(100),
    IN p_email VARCHAR(100),
    IN p_position VARCHAR(100),
    IN p_salary DECIMAL(10, 2)
)
BEGIN
    -- 1: READ
    IF p_flag = 1 THEN
        SELECT * FROM employees;

    -- 2: CREATE
    ELSEIF p_flag = 2 THEN
        INSERT INTO employees (name, email, position, salary) 
        VALUES (p_name, p_email, p_position, p_salary);
        SELECT LAST_INSERT_ID() AS id;

    -- 3: UPDATE
    ELSEIF p_flag = 3 THEN
        UPDATE employees 
        SET name = p_name, email = p_email, position = p_position, salary = p_salary 
        WHERE id = p_id;

    -- 4: DELETE
    ELSEIF p_flag = 4 THEN
        DELETE FROM employees WHERE id = p_id;
    END IF;
END$$

DELIMITER ;

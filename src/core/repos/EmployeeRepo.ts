import { Employee } from '@core/entities/Employee';

export interface EmployeeRepo {
    /**
     * Get all employees
     */
    getAllEmployees(): Employee[];

    /**
     * Get an employee by ID
     */
    getEmployee(employeeId: string): Employee;

    /**
     * Update an employee
     */
    updateEmployee(employee: Employee): void;

    /**
     * Add an employee
     */
    addEmployee(employee: Employee): void;
} 
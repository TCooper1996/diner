import { Employee } from '@core/entities/Employee';
import { EmployeeRepo } from '@core/repos/EmployeeRepo';

/**
 * Implementation of the EmployeeRepo interface that stores employees in a Map.
 */
export class EmployeeRepoImpl implements EmployeeRepo {
    private employees: Map<string, Employee>;

    constructor() {
        this.employees = new Map<string, Employee>();
    }

    getAllEmployees(): Employee[] {
        return Array.from(this.employees.values());
    }

    getEmployee(employeeId: string): Employee {
        const employee = this.employees.get(employeeId);
        if (!employee) {
            throw new Error(`No employee found with ID ${employeeId}`);
        }
        return employee;
    }

    updateEmployee(employee: Employee): void {
        this.employees.set(employee.name, employee);
    }

    addEmployee(employee: Employee): void {
        if (this.employees.has(employee.name)) {
            throw new Error(`Employee with ID ${employee.name} already exists`);
        }
        this.employees.set(employee.name, employee);
    }
} 
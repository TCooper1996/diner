import { EmployeeOrderRepo } from '@core/repos/EmployeeOrderRepo';

/**
 * Implementation of the EmployeeOrderRepo interface that stores the relationships
 * between employees and orders using Maps.
 * 
 * Since we need to track two distinct relationships (orders taken and orders carried),
 * we use two Maps to track each direction of the relationship.
 */
export class EmployeeOrderRepoImpl implements EmployeeOrderRepo {
    // Map of employee_name to a list of order_ids
    private employeeOrdersTaken: Map<string, string[]>;
    private employeeOrdersCarried: Map<string, string[]>;

    constructor() {
        this.employeeOrdersTaken = new Map<string, string[]>();
        this.employeeOrdersCarried = new Map<string, string[]>();
    }

    getOrdersTaken(employeeName: string): string[] {
        return this.employeeOrdersTaken.get(employeeName) || [];
    }

    addOrderTaken(employeeName: string, orderId: string): void {
        const orders = this.employeeOrdersTaken.get(employeeName) || [];
        if (!orders.includes(orderId)) {
            orders.push(orderId);
            this.employeeOrdersTaken.set(employeeName, orders);
        }
    }

    getOrdersCarried(employeeName: string): string[] {
        return this.employeeOrdersCarried.get(employeeName) || [];
    }

    addOrderCarried(employeeName: string, orderId: string): void {
        const orders = this.employeeOrdersCarried.get(employeeName) || [];
        if (!orders.includes(orderId)) {
            orders.push(orderId);
            this.employeeOrdersCarried.set(employeeName, orders);
        }
    }

    removeOrdersCarried(employeeName: string, orderId: string): void {
        const orders = this.employeeOrdersCarried.get(employeeName);
        if (orders) {
            const index = orders.indexOf(orderId);
            if (index !== -1) {
                orders.splice(index, 1);
                this.employeeOrdersCarried.set(employeeName, orders);
            }
        }
    }

    getEmployeeWithOrder(orderId: string): string | null {
        for (const [employeeName, orders] of this.employeeOrdersCarried.entries()) {
            if (orders.includes(orderId)) {
                return employeeName;
            }
        }
        return null;
    }
} 
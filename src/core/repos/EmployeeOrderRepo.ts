export interface EmployeeOrderRepo {
    /**
     * Get the orders taken by an employee
     */
    getOrdersTaken(employeeName: string): string[];

    /**
     * Add an order to the orders taken by an employee
     */
    addOrderTaken(employeeName: string, orderId: string): void;

    /**
     * Get the orders carried by an employee
     */
    getOrdersCarried(employeeName: string): string[];

    /**
     * Add an order to the orders carried by an employee
     */
    addOrderCarried(employeeName: string, orderId: string): void;

    /**
     * Remove an order from the orders carried by an employee
     */
    removeOrdersCarried(employeeName: string, orderId: string): void;
} 
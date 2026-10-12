/**
 * Represents whose turn it is in the game.
 * This can be either an employee or a customer.
 */
export type ActiveTurn = EmployeeUpdate | CustomerUpdate;

/**
 * Represents an employee's turn
 */
export interface EmployeeUpdate {
    type: 'EmployeeUpdate';
    name: string;
}

/**
 * Represents a customer's turn
 */
export interface CustomerUpdate {
    type: 'CustomerUpdate';
    name: string;
} 
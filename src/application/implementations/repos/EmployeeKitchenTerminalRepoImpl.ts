import { EmployeeKitchenTerminalRepo } from '@core/repos/EmployeeKitchenTerminalRepo';

/**
 * Implementation of the EmployeeKitchenTerminalRepo interface that manages the relationship
 * between employees and kitchen terminals using a Map.
 */
export class EmployeeKitchenTerminalRepoImpl implements EmployeeKitchenTerminalRepo {
    private employeeKitchenTerminals: Map<string, string>; // employee_id -> kitchen_terminal_id

    constructor() {
        this.employeeKitchenTerminals = new Map<string, string>();
    }

    getEmployeeKitchenTerminal(employeeId: string): string | null {
        return this.employeeKitchenTerminals.get(employeeId) || null;
    }

    addEmployeeKitchenTerminal(employeeId: string, kitchenTerminalId: string): void {
        // Check if the kitchen terminal is already assigned to another employee
        const terminalEmployee = this.getEmployeeOfKitchenTerminal(kitchenTerminalId);
        if (terminalEmployee && terminalEmployee !== employeeId) {
            throw new Error(`Kitchen terminal ${kitchenTerminalId} is already assigned to employee ${terminalEmployee}`);
        }
        
        // Set the new association
        this.employeeKitchenTerminals.set(employeeId, kitchenTerminalId);
    }

    removeEmployeeKitchenTerminal(employeeId: string): void {
        this.employeeKitchenTerminals.delete(employeeId);
    }

    private getEmployeeOfKitchenTerminal(kitchenTerminalId: string): string | null {
        for (const [employeeId, assignedTerminalId] of this.employeeKitchenTerminals.entries()) {
            if (assignedTerminalId === kitchenTerminalId) {
                return employeeId;
            }
        }
        return null;
    }
} 
import { Action } from '@core/models/Action';
import { ActionRepo } from '@core/repos/ActionRepo';

/**
 * Implementation of the ActionRepo interface that stores actions in a Map.
 */
export class ActionRepoImpl implements ActionRepo {
    private employeeActions: Map<string, Action | null>;

    constructor() {
        this.employeeActions = new Map<string, Action | null>();
    }

    setEmployeeAction(employeeId: string, action: Action | null): void {
        this.employeeActions.set(employeeId, action);
    }

    getEmployeeAction(employeeId: string): Action | null {
        return this.employeeActions.get(employeeId) || null;
    }
} 
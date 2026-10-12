import { ActionSelection } from '@core/models/ActionSelection';

export interface AgentService {
    /**
     * Get the next valid action for the given employee.
     */
    chooseAction(employeeName: string, stateMessage: string): Promise<ActionSelection>;
} 
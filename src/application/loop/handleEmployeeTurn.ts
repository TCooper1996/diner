import { Action, ValidationResult } from '@core/models/Action';
import { GameState } from '@core/models/GameState';
import { toPrompt } from '../implementations/misc/promptFromState';

/**
 * Handle an employee's turn in the game
 */
export async function handleEmployeeTurn(state: GameState, employeeId: string): Promise<void> {
    const action = await getNextAction(state, employeeId);

    const stateResult = action.execute(state, employeeId);
    state.logs.addTurnEffect(state.getTick(), stateResult.message);
    
    // Determine whether to continue with the action next time
    state.actions.setEmployeeAction(employeeId, stateResult.repeat ? action : null);
}

/**
 * Get the next action for an employee
 */
async function getNextAction(state: GameState, employeeId: string): Promise<Action> {
    const existingAction = state.actions.getEmployeeAction(employeeId);
    if (existingAction) {
        return existingAction;
    }

    for (let i = 0; i < 3; i++) {
        const selection = await state.agentService.chooseAction(employeeId, toPrompt(state.worldState));
        const result = selection.action.verify(state, employeeId);
        
        state.logs.addAgentInteraction(state.getTick(), selection.description, result.errorMsg || null);
        
        if (result.success) {
            return selection.action;
        }
    }

    throw new Error("No valid action selected after 3 attempts.");
} 
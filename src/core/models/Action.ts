export interface ActionResult {
    message: string;
    repeat?: boolean;
}

export interface ValidationResult {
    success: boolean;
    errorMsg?: string;
}

export interface Action {
    /**
     * Verify if the action is valid in the current state
     */
    verify(state: any, employeeId: string): ValidationResult;

    /**
     * Execute the action in the current state
     */
    execute(state: any, employeeId: string): ActionResult;
} 
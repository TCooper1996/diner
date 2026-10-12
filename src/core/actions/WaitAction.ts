import { ActionResult, ValidationResult } from "../models/Action";

export interface WaitActionMethods {}

export function waitAction(methods: WaitActionMethods, employeeId: string): ActionResult {
    return {
        message: `${employeeId} is waiting for the next instruction.`,
        repeat: false
    };
}
export interface WaitActionValidationMethods {}
export function validationWaitAction(methods: WaitActionValidationMethods, employeeId: string): ValidationResult {
    return {
        success: true,
    };
} 
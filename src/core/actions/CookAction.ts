import { ValidationResult } from "../models/Action";
import { ActionResult } from "./shared";

export interface CookActionParams {
    order_id: string;
}

export interface CookActionMethods {
    find_unoccupied_grill(employeeId: string): string
    step_toward_grill(employeeId: string, grill: string): void
    grill_reached(employeeId: string): boolean
    cook_order(employeeId: string, order_id: string): void
    order_cooked(employeeId: string, order_id: string): boolean
}

export function cookAction(methods: CookActionMethods, employeeId: string, params: CookActionParams): ActionResult {
    const grill = methods.find_unoccupied_grill(employeeId)
    if (!methods.grill_reached(employeeId)){
        methods.step_toward_grill(employeeId, grill)
        return {
            message: `${employeeId} is moving toward the kitchen to cook order ${params.order_id}.`,
            repeat: true
        };
    } 

    methods.cook_order(employeeId, params.order_id)
    if (!methods.order_cooked(employeeId, params.order_id)){
        return {
            message: `${employeeId} is cooking order ${params.order_id}.`,
            repeat: true
        };
    } 
    
    return {
        message: `${employeeId} cooked order ${params.order_id}.`,
        repeat: false
    };
    
    
}


export interface CookActionValidationMethods{
    order_exists(order_id: string): boolean
    is_order_submitted(order_id: string): boolean
}

export function validationCookAction(methods: CookActionValidationMethods, employeeId: string, params: CookActionParams): ValidationResult{
    if (!methods.order_exists(params.order_id)){
        return {
            success: false,
            errorMsg: `Order ${params.order_id} does not exist.`
        };
    }

    if (!methods.is_order_submitted(params.order_id)){
        return {
            success: false,
            errorMsg: `Order ${params.order_id} has not been submitted or has already been cooked.`
        };
    }

    return {
        success: true,
    };
}
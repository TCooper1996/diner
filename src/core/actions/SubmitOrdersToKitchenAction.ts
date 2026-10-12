import { ActionResult, ActionValidationResult } from './shared';
import { Order } from '@core/entities/Order';

export interface SubmitOrdersToKitchenParams {}

export interface SubmitOrdersToKitchenMethods {
    get_orders_to_submit(employeeId: string): string[];
    find_unoccupied_grill(employeeId: string): string
    step_toward_grill(employeeId: string, grill: string): void;
    grill_reached(employeeId: string): boolean;
    submit_orders(employeeId: string): void;
}

export function submitOrdersToKitchenAction(methods: SubmitOrdersToKitchenMethods, employeeId: string, params: SubmitOrdersToKitchenParams): ActionResult {
    const grill = methods.find_unoccupied_grill(employeeId)
    methods.step_toward_grill(employeeId, grill)

    if (methods.grill_reached(employeeId)){
        methods.submit_orders(employeeId);
        return {
            message: `Submitted ${methods.get_orders_to_submit(employeeId).length} orders to kitchen`,
            repeat: false
        };
    } else {
        return {
            message: `${employeeId} is bringing orders to the kitchen.`,
            repeat: true
        };
    }
}

export interface SubmitOrdersToKitchenValidationMethods {
    get_orders_to_submit(employeeId: string): string[];
}

export function validateSubmitOrdersToKitchenAction(methods: SubmitOrdersToKitchenValidationMethods, employeeId: string, params: SubmitOrdersToKitchenParams): ActionValidationResult {
    if (methods.get_orders_to_submit(employeeId).length === 0) {
        return {
            success: false,
            error_message: `${employeeId} has no pending orders to submit to the kitchen.`
        };
    }
    return { success: true };
} 
import { ActionResult, ActionValidationResult } from "./shared";

export interface SeatActionParams {
    customer_id: string;
}

export interface SeatActionMethods {
    reached_seat(employeeId: string, customerId: string): boolean;
    seat_customer(employeeId: string, customerId: string): void;
    step_toward_seat(employeeId: string, customerId: string): void;
}


export function seatAction(methods: SeatActionMethods, employeeId: string, params: SeatActionParams): ActionResult {

    methods.step_toward_seat(employeeId, params.customer_id);

    if (methods.reached_seat(employeeId, params.customer_id)) {
        methods.seat_customer(employeeId, params.customer_id);
        return {
            message: `${employeeId} seated customer ${params.customer_id}.`,
            repeat: false
        };
    } else {
        return {
            message: `${employeeId} is moving toward seat for customer: ${params.customer_id}.`,
            repeat: true
        };
    }
} 

export interface SeatActionValidationMethods {
    customer_exists(customerId: string): boolean;
}
export function validateSeatAction(methods: SeatActionValidationMethods, params: SeatActionParams): ActionValidationResult {

    if (!methods.customer_exists(params.customer_id)) {
        return {
            success: false,
            error_message: `Customer ${params.customer_id} does not exist.`
        };
    }

    return {
        success: true
    };
}
import { ActionResult, ValidationResult } from "../models/Action";

export interface PickUpOrderParams {
    order_id: string;
}

export interface PickUpOrderMethods {
    order_exists(order_id: string): boolean;
    is_order_ready(order_id: string): boolean;
    find_pickup_counter(employeeId: string): string;
    pickup_counter_reached(employeeId: string, pickup_counter: string): boolean;
    add_order_to_inventory(employeeId: string, order_id: string): void;
    step_toward_pickup_counter(employeeId: string, pickup_counter: string): void;
}

export function pickUpOrderAction(methods: PickUpOrderMethods, employeeId: string, params: PickUpOrderParams): ActionResult {

    const pickup_counter = methods.find_pickup_counter(employeeId);
    if (!methods.pickup_counter_reached(employeeId, pickup_counter)) {
        methods.step_toward_pickup_counter(employeeId, pickup_counter);
        return {
            message: `${employeeId} is moving toward the pickup counter.`,
            repeat: true
        };
    }

    methods.add_order_to_inventory(employeeId, params.order_id);
    return {
        message: `${employeeId} picked up order ${params.order_id}.`,
        repeat: false
    };
}

export interface PickUpOrderValidationMethods {
    order_exists(order_id: string): boolean;
    is_order_ready(order_id: string): boolean;
}

export function validationPickUpOrderAction(methods: PickUpOrderValidationMethods, employeeId: string, params: PickUpOrderParams): ValidationResult {
    if (!methods.order_exists(params.order_id)) {
        return {
            success: false,
            errorMsg: `There is no order named ${params.order_id}.`
        };
    }

    if (!methods.is_order_ready(params.order_id)) {
        return {
            success: false,
            errorMsg: `The order ${params.order_id} is not ready for ${employeeId} to pick up.`
        };
    }

    return {
        success: true,
    };
} 
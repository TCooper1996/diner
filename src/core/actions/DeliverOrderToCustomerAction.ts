import { ActionResult, ValidationResult } from "../models/Action";

export interface DeliverOrderToCustomerParams {
    customer_id: string;
    order_id: string;
}

export interface DeliverOrderToCustomerMethods {
    has_order_in_inventory(employeeId: string, order_id: string): boolean;
    customer_exists(customer_id: string): boolean;
    step_toward_customer(employeeId: string, customer_id: string): void;
    reached_customer(employeeId: string, customer_id: string): boolean;
    update_order_status(order_id: string, status: string): void;
    update_customer_status(customer_id: string, status: string): void;
    complete_order_delivery(employeeId: string, order_id: string, customer_id: string): void;
}

export function deliverOrderToCustomerAction(methods: DeliverOrderToCustomerMethods, employeeId: string, params: DeliverOrderToCustomerParams): ActionResult {

    if (!methods.reached_customer(employeeId, params.customer_id)) {
        methods.step_toward_customer(employeeId, params.customer_id);
        return {
            message: `${employeeId} is moving toward customer: ${params.customer_id} to deliver order #${params.order_id}.`,
            repeat: true
        };
    }
    
    methods.complete_order_delivery(employeeId, params.order_id, params.customer_id);

    return {
        message: `${employeeId} delivered order #${params.order_id} to customer ${params.customer_id}. The customer is now eating.`,
        repeat: false
    };
}

export interface DeliverOrderToCustomerValidationMethods {
    has_order_in_inventory(employeeId: string, order_id: string): boolean;
    customer_exists(customer_id: string): boolean;
}

export function validationDeliverOrderToCustomerAction(methods: DeliverOrderToCustomerValidationMethods, employeeId: string, params: DeliverOrderToCustomerParams): ValidationResult {
    if (!methods.has_order_in_inventory(employeeId, params.order_id)) {
        return {
            success: false,
            errorMsg: `${employeeId} does not have order ${params.order_id} in their inventory.`
        };
    }

    if (!methods.customer_exists(params.customer_id)) {
        return {
            success: false,
            errorMsg: `Customer ${params.customer_id} does not exist.`
        };
    }

    return {
        success: true,
    };
}

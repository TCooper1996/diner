export interface TakeOrderActionParams {
    customer_id: string
}

export interface TakeOrderActionMethods {
    reached_customer(employeeId: string, customerId: string): boolean
    take_order_from_customer(employeeId: string, customerId: string): void
    step_toward_customer(employeeId: string, customerId: string): void
}

export interface TakeOrderActionValidationMethods {
    customer_exists(customerId: string): boolean
}

export function takeOrderAction(methods: TakeOrderActionMethods, employeeId: string, params: TakeOrderActionParams){

    methods.step_toward_customer(employeeId, params.customer_id);
    
    if (methods.reached_customer(employeeId, params.customer_id)) {
      methods.take_order_from_customer(employeeId, params.customer_id);
      return {
        message: `${employeeId} took an order from customer ${params.customer_id}`,
        repeat: false
      };
    } else {
      return {
        message: `${employeeId} is moving toward customer: ${params.customer_id} to take order.`,
        repeat: true
      };
    }
}

export function validateTakeOrderAction(methods: TakeOrderActionValidationMethods, params: TakeOrderActionParams): string | null {
    if (!methods.customer_exists(params.customer_id)) {
        return `Customer ${params.customer_id} does not exist.`;
    }
    return null;
}
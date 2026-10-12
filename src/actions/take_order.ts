import { RestaurantState } from '../core/models/RestaurantState';
import { ActionResult, ValidationResult } from '../core/models/Action';
import { ActionDefinition } from './types';
import { TakeOrderActionMethods, TakeOrderActionParams } from '@/core/actions/TakeOrderAction';

export const takeOrderAction: ActionDefinition = {
  name: 'takeOrder',
  description: 'Take a customers order.',
  parameters: {
    type: 'object',
    properties: {
      customer_id: {
        type: 'string',
        description: 'The ID of the customer to take order from'
      }
    },
    required: ['customer_id']
  }
};


export const takeOrderHandler = {
  validate: (methods: TakeOrderActionMethods, employeeId: string, params: TakeOrderActionParams): ValidationResult => {
    if (!methods.customer_exists(params.customer_id)) {
      return {
        success: false,
        errorMsg: `Customer ${params.customer_id} not found.`
      };
    }
    
    return { success: true };
  },

  execute: (methods: TakeOrderActionMethods, employeeId: string, params: TakeOrderActionParams): ActionResult => {
  }
}; 

// Utilities --------------------------------
function customer_exists(state: RestaurantState, customerId: string): boolean {
  try {
    state.customers.getCustomer(customerId);
    return true;
  } catch {
    return false;
  }
}

function step_toward_customer(state: RestaurantState, employeeId: string, customerId: string): void {
  const customer = state.customers.getCustomer(customerId);
  const employee = state.employees.getEmployee(employeeId);
  const path = state.getNavigationService().getPathBetweenPositions(employee.position, customer.position);
  
  if (path && path.length > 1) {
    const newPosition = {x: path[1].x, y: path[1].y}
    state.employees.updateEmployee({
      ...employee,
      position: newPosition
    });
  }
}



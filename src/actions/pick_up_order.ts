import { RestaurantState } from '@core/models/RestaurantState';
import { ActionResult, ValidationResult } from '@core/models/Action';
import { ActionDefinition, ActionHandler } from './types';
import { OrderStatus, Order } from '@core/entities/Order';
import { Employee } from '@core/entities/Employee';
import { Grill } from '@core/entities/Grill';
import { Position, positions_are_equal } from '@core/common/Position';

export const pickUpOrderAction: ActionDefinition = {
  name: 'pickUpOrder',
  description: 'Adds a nearby order to your inventory. You must be in the kitchen to pick up an order. You can only pick up orders that are ready.',
  parameters: {
    type: 'object',
    properties: {
      order_id: {
        type: 'string',
        description: 'The ID of the order to pick up. Must be in the kitchen.'
      }
    },
    required: ['order_id']
  }
};

export interface PickUpOrderState extends 
    Pick<RestaurantState, 'getNavigationService' | 'orders' | 'employees' | 'grills' | 'employeeOrders'>
{}


export type PickUpOrderParams = {
  order_id: string;
}

export const pickUpOrderHandler = {
  validate: (state: RestaurantState, employeeId: string, params: PickUpOrderParams): ValidationResult => {
    if (!order_exists(state, params.order_id)) {
      return {
        success: false,
        errorMsg: `There is no order named ${params.order_id}.`
      };
    }
    
    if (!is_order_ready(state, params.order_id)) {
      return {
        success: false,
        errorMsg: `The order ${params.order_id} is not ready for ${employeeId} to pick up.`
      };
    }
    
    return { success: true };
  },

  execute: (state: PickUpOrderState, employeeId: string, params: PickUpOrderParams): ActionResult => {
    // For now, we just pick up the order at the nearest grill.
    const grill = find_nearest_grill(state, employeeId);
    if (!is_at_grill(state, employeeId, grill)) {
      step_toward_kitchen(state, employeeId);
      return {
        message: `${employeeId} is moving toward the kitchen.`,
        repeat: true
      };
    }
    add_order_to_inventory(state, employeeId, params.order_id);
    return {
      message: `${employeeId} picked up order ${params.order_id}.`,
      repeat: false
    };
  }
};

// Utilities --------------------------------
function order_exists(state: PickUpOrderState, orderId: string): boolean {
  try {
    state.orders.getOrder(orderId);
    return true;
  } catch {
    return false;
  }
}

function is_order_ready(state: PickUpOrderState, orderId: string): boolean {
  const order = state.orders.getOrder(orderId);
  return order.status === OrderStatus.READY;
}

function is_at_grill(state: PickUpOrderState, employeeId: string, grill: Grill): boolean {
  return positions_are_equal(state.employees.getEmployee(employeeId).position, grill.position)
}

function add_order_to_inventory(state: PickUpOrderState, employeeId: string, orderId: string): void {
  state.employeeOrders.addOrderCarried(employeeId, orderId);
}

function step_toward_kitchen(state: PickUpOrderState, employeeId: string): void {
  const employee = state.employees.getEmployee(employeeId);
  const grills = state.grills.getAllGrills();
  const grillPositions = grills.map(g => g.position);
  const nearestIndex = state.getNavigationService().getClosestEntity(employee.position, grillPositions);
  const newPosition = state.getNavigationService().moveToward(employee.position, grillPositions[nearestIndex]);
  
  const updatedEmployee = new Employee(
    employee.name,
    newPosition
  );
  state.employees.updateEmployee(updatedEmployee);
} 

function find_nearest_grill(state: PickUpOrderState, employeeId: string): Grill {
  const employee = state.employees.getEmployee(employeeId);
  const grills = state.grills.getAllGrills();
  const grillPositions = grills.map(g => g.position);
  const nearestIndex = state.getNavigationService().getClosestEntity(employee.position, grillPositions);
  return state.grills.getGrill(grills[nearestIndex].grillId)
}
import { RestaurantState } from '../core/models/RestaurantState';
import { ActionResult, ValidationResult } from '../core/models/Action';
import { ActionDefinition, ActionHandler } from './types';
import { Order, OrderStatus } from '../core/entities/Order';
import { Position } from '../core/common/Position';
import { Grill } from '../core/entities/Grill';

export const submitOrdersToKitchenAction: ActionDefinition = {
  name: 'submitOrdersToKitchen',
  description: 'Notify kitchen of new orders',
  parameters: {
    type: 'object',
    properties: {},
    required: []
  }
};

export type SubmitOrdersToKitchenParams = {}

export const submitOrdersToKitchenHandler: ActionHandler = {
  validate: (state: RestaurantState, employeeId: string, params: SubmitOrdersToKitchenParams): ValidationResult => {
    if (get_orders_to_submit(state, employeeId).length === 0) {
      return {
        success: false,
        errorMsg: `${employeeId} has no pending orders to submit to the kitchen.`
      };
    }
    return { success: true };
  },

  execute: (state: RestaurantState, employeeId: string, params: SubmitOrdersToKitchenParams): ActionResult => {
    const grill = get_or_find_grill(state, employeeId);
    step_toward_grill(state, employeeId, grill.position);

    if (grill_reached(state, employeeId, grill.position)) {
      submit_orders(state, employeeId);
      return {
        message: `Submitted ${get_orders_to_submit(state, employeeId).length} orders to kitchen`,
        repeat: false
      };
    } else {
      return {
        message: `${employeeId} is bringing orders to the kitchen.`,
        repeat: true
      };
    }
  }
};

// Utilities --------------------------------
function get_orders_to_submit(state: RestaurantState, employeeId: string): Order[] {
  const orders = state.orders.getAllOrders();
  return orders.filter(order => order.isPending());
}

function get_or_find_grill(state: RestaurantState, employeeId: string): Grill {
  const grillId = state.employeeGrills.getEmployeeGrill(employeeId);
  if (grillId) {
    return state.grills.getGrill(grillId);
  }
  
  const grill = find_nearest_unoccupied_grill(state, employeeId);
  state.employeeGrills.setEmployeeGrill(employeeId, grill.grillId);
  return grill;
}

function find_nearest_unoccupied_grill(state: RestaurantState, employeeId: string): Grill {
  const employee = state.employees.getEmployee(employeeId);
  const grills = state.grills.getAllGrills();
  const unoccupiedGrills = grills.filter(g => !state.employeeGrills.getEmployeeGrill(g.grillId));
  
  if (unoccupiedGrills.length === 0) {
    throw new Error('No unoccupied grills available');
  }
  
  let nearestGrill = unoccupiedGrills[0];
  let shortestPath = state.getNavigationService().getPathBetweenPositions(employee.position, nearestGrill.position);
  let shortestPathLength = shortestPath ? shortestPath.length : Infinity;
  
  for (const grill of unoccupiedGrills.slice(1)) {
    const path = state.getNavigationService().getPathBetweenPositions(employee.position, grill.position);
    if (path && path.length < shortestPathLength) {
      nearestGrill = grill;
      shortestPathLength = path.length;
    }
  }
  
  return nearestGrill;
}

function step_toward_grill(state: RestaurantState, employeeId: string, grillPosition: Position): void {
  const employee = state.employees.getEmployee(employeeId);
  const path = state.getNavigationService().getPathBetweenPositions(employee.position, grillPosition);
  
  if (path && path.length > 1) {
    const newPosition = { x: path[1].x, y: path[1].y };
    state.employees.updateEmployee({
      ...employee,
      position: newPosition
    });
  }
}

function grill_reached(state: RestaurantState, employeeId: string, grillPosition: Position): boolean {
  const employee = state.employees.getEmployee(employeeId);
  return employee.position.x === grillPosition.x && employee.position.y === grillPosition.y;
}

function submit_orders(state: RestaurantState, employeeId: string): void {
  const orders = get_orders_to_submit(state, employeeId);
  for (const order of orders) {
    order.status = OrderStatus.COOKING;
    state.orders.updateOrder(order);
  }
} 
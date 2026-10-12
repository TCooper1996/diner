import { RestaurantState, Position, Customer, Order, ValidationResult } from './types';

export function customer_exists(state: RestaurantState, customerId: string): boolean {
  try {
    state.get_customer(customerId);
    return true;
  } catch {
    return false;
  }
}

export function order_exists(state: RestaurantState, orderId: string): boolean {
  try {
    state.get_order(orderId);
    return true;
  } catch {
    return false;
  }
}

export function reached_customer(state: RestaurantState, employeeId: string, customerId: string): boolean {
  const employee = state.get_employee(employeeId);
  const customer = state.get_customer(customerId);
  return positions_are_equal(employee.position, customer.position);
}

export function positions_are_equal(pos1: Position, pos2: Position): boolean {
  return pos1.x === pos2.x && pos1.y === pos2.y;
}

export function step_toward_customer(state: RestaurantState, employeeId: string, customerId: string): void {
  const customer = state.get_customer(customerId);
  const employee = state.get_employee(employeeId);
  const path = state.get_navigation_service().get_path_between_positions(employee.position, customer.position);
  
  if (path && path.length > 1) {
    employee.position = path[1];
    state.update_employee(employee);
  }
}

export function find_nearest_unoccupied_grill(state: RestaurantState, employeeId: string): Grill {
  const employee = state.get_employee(employeeId);
  const grills = state.get_all_grills();
  const unoccupiedGrills = grills.filter(g => !state.is_grill_occupied(g.grill_id));
  
  if (unoccupiedGrills.length === 0) {
    throw new Error('No unoccupied grills available');
  }
  
  let nearestGrill = unoccupiedGrills[0];
  let shortestPath = state.get_navigation_service().get_path_between_positions(employee.position, nearestGrill.position);
  let shortestPathLength = shortestPath ? shortestPath.length : Infinity;
  
  for (const grill of unoccupiedGrills.slice(1)) {
    const path = state.get_navigation_service().get_path_between_positions(employee.position, grill.position);
    if (path && path.length < shortestPathLength) {
      nearestGrill = grill;
      shortestPathLength = path.length;
    }
  }
  
  return nearestGrill;
}

export function step_toward_grill(state: RestaurantState, employeeId: string, grill: Grill): void {
  const employee = state.get_employee(employeeId);
  const path = state.get_navigation_service().get_path_between_positions(employee.position, grill.position);
  
  if (path && path.length > 1) {
    employee.position = path[1];
    state.update_employee(employee);
  }
}

export function grill_reached(state: RestaurantState, employeeId: string, grill: Grill): boolean {
  const employee = state.get_employee(employeeId);
  return positions_are_equal(employee.position, grill.position);
} 
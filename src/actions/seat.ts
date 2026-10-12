import { RestaurantState } from '../core/models/RestaurantState';
import { ActionResult, ValidationResult } from '../core/models/Action';
import { ActionDefinition, ActionHandler } from './types';
import { CustomerStatus, Customer } from '../core/entities/Customer';
import { Position } from '../core/common/Position';
import { Seat } from '../core/entities/Seat';

export const seatAction: ActionDefinition = {
  name: 'seat',
  description: 'Take a seat',
  parameters: {
    type: 'object',
    properties: {
      customer_id: {
        type: 'string',
        description: 'The ID of the customer to seat'
      }
    },
    required: ['customer_id']
  }
};

export type SeatParams = {
  customer_id: string;
}

export const seatHandler: ActionHandler = {
  validate: (state: RestaurantState, employeeId: string, params: SeatParams): ValidationResult => {
    if (!customer_exists(state, params.customer_id)) {
      return {
        success: false,
        errorMsg: `Customer ${params.customer_id} does not exist.`
      };
    }
    if (get_customer_status(state, params.customer_id) !== CustomerStatus.WAITING) {
      return {
        success: false,
        errorMsg: `Customer ${params.customer_id} is not waiting.`
      };
    }
    
    return { success: true };
  },

  execute: (state: RestaurantState, employeeId: string, params: SeatParams): ActionResult => {
    const seat = get_or_find_customer_seat(state, params.customer_id);
    step_toward_chair(state, params.customer_id, seat);

    if (arrived_at_chair(state, params.customer_id, seat)) {
      return {
        message: `Customer ${params.customer_id} is now seated at table.`,
        repeat: false
      };
    }

    return {
      message: `${employeeId} is leading ${params.customer_id} to a table.`,
      repeat: true
    };
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

function get_customer_status(state: RestaurantState, customerId: string): CustomerStatus {
  const customer = state.customers.getCustomer(customerId);
  return customer.status;
}

function get_or_find_customer_seat(state: RestaurantState, customerId: string): Seat {
  const seatId = state.customerSeats.getCustomerSeat(customerId);
  if (seatId) {
    return state.seats.getSeat(seatId);
  }

  const customer = state.customers.getCustomer(customerId);
  const seats = state.seats.getAllSeats();
  const unoccupiedSeats = seats.filter(s => !state.customerSeats.isSeatOccupied(s.seatId));
  
  if (unoccupiedSeats.length === 0) {
    throw new Error('No unoccupied seats available');
  }

  const seatIndex = state.getNavigationService().getClosestEntity(customer.position, unoccupiedSeats.map(s => s.position));
  const selectedSeat = unoccupiedSeats[seatIndex];
  state.customerSeats.setCustomerSeat(customerId, selectedSeat.seatId);

  return selectedSeat;
}

function step_toward_chair(state: RestaurantState, customerId: string, seat: Seat): void {
  const customer = state.customers.getCustomer(customerId);
  const path = state.getNavigationService().getPathBetweenPositions(customer.position, seat.position);
  
  if (path && path.length > 1) {
    const newPosition = { x: path[1].x, y: path[1].y };
    const updatedCustomer = new Customer(
      customer.id,
      newPosition,
      customer.waitingTime,
      customer.patience,
      customer.status,
      customer.eatingTime
    );
    state.customers.updateCustomer(updatedCustomer);
  }
}

function arrived_at_chair(state: RestaurantState, customerId: string, seat: Seat): boolean {
  const customer = state.customers.getCustomer(customerId);
  return customer.position.x === seat.position.x && customer.position.y === seat.position.y;
} 
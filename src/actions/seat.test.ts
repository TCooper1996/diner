import { describe, it, expect, beforeEach } from 'vitest';
import { CustomerStatus, Customer } from '@core/entities/Customer';
import { Seat } from '@core/entities/Seat';
import { seatAction, seatHandler, SeatParams } from './seat';
import { TestRestaurantState } from '@test_utils/TestRestaurantState';

describe('seat action', () => {
  let mockState: TestRestaurantState;
  const employeeId = 'employee1';
  const customerId = 'customer1';
  const seatId = 'seat1';

  beforeEach(() => {
    mockState = new TestRestaurantState();
  });

  describe('action definition', () => {
    it('should have correct name and description', () => {
      expect(seatAction.name).toBe('seat');
      expect(seatAction.description).toBe('Take a seat');
    });

    it('should require customer_id parameter', () => {
      expect(seatAction.parameters.required).toContain('customer_id');
    });
  });

  describe('validate', () => {
    it('should return error if customer does not exist', () => {
      const result = seatHandler.validate(mockState, employeeId, { customer_id: customerId });
      expect(result.success).toBe(false);
      expect(result.errorMsg).toContain('does not exist');
    });

    it('should return error if customer is not waiting', () => {
      const mockCustomer = new Customer(
        customerId,
        { x: 0, y: 0 },
        0,
        50,
        CustomerStatus.SEATED,
        0
      );
      mockState.customers.addCustomer(mockCustomer);

      const result = seatHandler.validate(mockState, employeeId, { customer_id: customerId });
      expect(result.success).toBe(false);
      expect(result.errorMsg).toContain('not waiting');
    });

    it('should return success if validation passes', () => {
      const mockCustomer = new Customer(
        customerId,
        { x: 0, y: 0 },
        0,
        50,
        CustomerStatus.WAITING,
        0
      );
      mockState.customers.addCustomer(mockCustomer);

      const result = seatHandler.validate(mockState, employeeId, { customer_id: customerId });
      expect(result.success).toBe(true);
    });
  });

  describe('execute', () => {
    const mockSeat = new Seat(seatId, { x: 5, y: 5 });
    const mockCustomer = new Customer(
      customerId,
      { x: 0, y: 0 },
      0,
      50,
      CustomerStatus.WAITING,
      0
    );

    beforeEach(() => {
      mockState.customers.addCustomer(mockCustomer);
      mockState.seats.addSeat(mockSeat);
      mockState.getMockNavigationService().getClosestEntity.mockReturnValue(0);
      mockState.getMockNavigationService().getPathBetweenPositions.mockReturnValue([
        { x: 0, y: 0 },
        { x: 1, y: 1 }
      ]);
    });

    it('should move customer toward seat and return repeat true', () => {
      const result = seatHandler.execute(mockState, employeeId, { customer_id: customerId });
      
      expect(result.repeat).toBe(true);
      expect(result.message).toContain('leading');
      expect(mockState.customers.getCustomer(customerId)?.position).toEqual({ x: 1, y: 1 });
    });

    it('should seat customer when reached and return repeat false', () => {
      mockState.getMockNavigationService().getPathBetweenPositions.mockReturnValue([
        { x: 5, y: 5 }
      ]);

      const result = seatHandler.execute(mockState, employeeId, { customer_id: customerId });
      
      expect(result.repeat).toBe(false);
      expect(result.message).toContain('now seated');
      expect(mockState.customerSeats.getCustomerSeat(customerId)).toBe(seatId);
    });
  });
}); 
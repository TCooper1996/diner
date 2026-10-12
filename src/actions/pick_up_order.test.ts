import { describe, it, expect, beforeEach } from 'vitest';
import { OrderStatus, Order } from '@core/entities/Order';
import { Employee } from '@core/entities/Employee';
import { Grill } from '@core/entities/Grill';
import { pickUpOrderAction, pickUpOrderHandler, PickUpOrderParams, PickUpOrderState } from './pick_up_order';
import { TestRestaurantState } from '@test_utils/TestRestaurantState';

describe('pick_up_order action', () => {
  let mockState: PickUpOrderState;
  const employeeId = 'employee1';
  const orderId = 'order1';
  const grillId = 'grill1';

  beforeEach(() => {
    mockState = new TestRestaurantState();
  });

  describe('action definition', () => {
    it('should have correct name and description', () => {
      expect(pickUpOrderAction.name).toBe('pick_up_order');
      expect(pickUpOrderAction.description).toBe('Pick up an order from the kitchen');
    });

    it('should require order_id parameter', () => {
      expect(pickUpOrderAction.parameters.required).toContain('order_id');
    });
  });

  describe('validate', () => {
    it('should return error if order does not exist', () => {
      const result = pickUpOrderHandler.validate(mockState, employeeId, { order_id: orderId });
      expect(result.success).toBe(false);
      expect(result.errorMsg).toContain('does not exist');
    });

    it('should return error if order is not ready', () => {
      const mockOrder = new Order(orderId, OrderStatus.COOKING);
      mockState.orders.addOrder(mockOrder);

      const result = pickUpOrderHandler.validate(mockState, employeeId, { order_id: orderId });
      expect(result.success).toBe(false);
      expect(result.errorMsg).toContain('not ready');
    });

    it('should return success if validation passes', () => {
      const mockOrder = new Order(orderId, OrderStatus.READY);
      mockState.orders.addOrder(mockOrder);

      const result = pickUpOrderHandler.validate(mockState, employeeId, { order_id: orderId });
      expect(result.success).toBe(true);
    });
  });

  describe('execute', () => {
    const mockOrder = new Order(orderId, OrderStatus.READY);
    const mockEmployee = new Employee('employee1', { x: 0, y: 0 });
    const mockGrill = new Grill(grillId, { x: 5, y: 5 });

    beforeEach(() => {
      mockState.orders.addOrder(mockOrder);
      mockState.employees.addEmployee(mockEmployee);
      mockState.grills.addGrill(mockGrill);
      mockState.getMockNavigationService().getClosestEntity.mockReturnValue(0);
      mockState.getMockNavigationService().getPathBetweenPositions.mockReturnValue([
        { x: 0, y: 0 },
        { x: 1, y: 1 }
      ]);
    });

    it('should move employee toward kitchen and return repeat true', () => {
      const state: PickUpOrderState = {
        orders: mockState.orders,
        employees: mockState.employees,
        grills: mockState.grills,
        employeeOrders: mockState.employeeOrders,
        getNavigationService: mockState.getNavigationService
      }
      mockState.getMockNavigationService().getClosestEntity.mockReturnValue(0);
      const result = pickUpOrderHandler.execute(mockState, employeeId, { order_id: orderId });
      
      expect(result.repeat).toBe(true);
      expect(result.message).toContain('moving');
      expect(mockState.employees.getEmployee(employeeId)?.position).toEqual({ x: 1, y: 1 });
    });

    it('should pick up order when reached and return repeat false', () => {
      mockState.getMockNavigationService().getPathBetweenPositions.mockReturnValue([
        { x: 5, y: 5 }
      ]);

      const result = pickUpOrderHandler.execute(mockState, employeeId, { order_id: orderId });
      
      expect(result.repeat).toBe(false);
      expect(result.message).toContain('picked up');
      expect(mockState.employeeOrders.getOrdersCarried(employeeId)).toContain(orderId);
    });
  });
}); 
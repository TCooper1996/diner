import { RestaurantState } from '@core/models/RestaurantState';
import { RestaurantStateImpl } from '@application/implementations/models/RestaurantStateImpl';
import { NavigationService } from '@core/services/NavigationService';
import { CustomerRepoImpl } from '@application/implementations/repos/CustomerRepoImpl';
import { OrderRepoImpl } from '@application/implementations/repos/OrderRepoImpl';
import { EmployeeRepoImpl } from '@application/implementations/repos/EmployeeRepoImpl';
import { SeatRepoImpl } from '@application/implementations/repos/SeatRepoImpl';
import { EntranceRepoImpl } from '@application/implementations/repos/EntranceRepoImpl';
import { GrillRepoImpl } from '@application/implementations/repos/GrillRepoImpl';
import { CustomerSeatRepoImpl } from '@application/implementations/repos/CustomerSeatRepoImpl';
import { CustomerOrderRepoImpl } from '@application/implementations/repos/CustomerOrderRepoImpl';
import { EmployeeGrillRepoImpl } from '@application/implementations/repos/EmployeeGrillRepoImpl';
import { EmployeeOrderRepoImpl } from '@application/implementations/repos/EmployeeOrderRepoImpl';
import { EmployeeKitchenTerminalRepoImpl } from '@application/implementations/repos/EmployeeKitchenTerminalRepoImpl';
import { vi, Mock } from 'vitest';

export class TestRestaurantState extends RestaurantStateImpl {
  constructor() {
    const mockNavigationService = {
      getPathBetweenPositions: vi.fn(),
      getClosestEntity: vi.fn(),
      moveToward: vi.fn()
    } as unknown as NavigationService;

    super(
      mockNavigationService,
      new CustomerRepoImpl(),
      new OrderRepoImpl(),
      new EmployeeRepoImpl(),
      new SeatRepoImpl(),
      new EntranceRepoImpl(),
      new GrillRepoImpl(),
      new CustomerSeatRepoImpl(),
      new CustomerOrderRepoImpl(),
      new EmployeeGrillRepoImpl(),
      new EmployeeOrderRepoImpl(),
      new EmployeeKitchenTerminalRepoImpl()
    );
  }

  // Helper method to access mock navigation service
  getMockNavigationService() {
    return this.getNavigationService() as unknown as {
      getPathBetweenPositions: Mock;
      getClosestEntity: Mock;
      moveToward: Mock;
    };
  }
} 
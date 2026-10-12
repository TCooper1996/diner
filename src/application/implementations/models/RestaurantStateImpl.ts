import { RestaurantState } from '@core/models/RestaurantState';
import { NavigationService } from '@core/services/NavigationService';
import { OrderRepoImpl } from '../repos/OrderRepoImpl';
import { EmployeeRepoImpl } from '../repos/EmployeeRepoImpl';
import { SeatRepoImpl } from '../repos/SeatRepoImpl';
import { EntranceRepoImpl } from '../repos/EntranceRepoImpl';
import { GrillRepoImpl } from '../repos/GrillRepoImpl';
import { CustomerSeatRepoImpl } from '../repos/CustomerSeatRepoImpl';
import { CustomerOrderRepoImpl } from '../repos/CustomerOrderRepoImpl';
import { EmployeeGrillRepoImpl } from '../repos/EmployeeGrillRepoImpl';
import { EmployeeOrderRepoImpl } from '../repos/EmployeeOrderRepoImpl';
import { CustomerRepoImpl } from '../repos/CustomerRepoImpl';
import { EmployeeKitchenTerminalRepoImpl } from '../repos/EmployeeKitchenTerminalRepoImpl';

/**
 * RestaurantStateImpl implements the RestaurantState interface using composition.
 * It combines all repository implementations into a single state object.
 */
export class RestaurantStateImpl implements RestaurantState {

    constructor(private readonly navigationService: NavigationService, 
        public readonly customers: CustomerRepoImpl,
        public readonly orders: OrderRepoImpl,
        public readonly employees: EmployeeRepoImpl,
        public readonly seats: SeatRepoImpl,
        public readonly entrances: EntranceRepoImpl,
        public readonly grills: GrillRepoImpl,
        public readonly customerSeats: CustomerSeatRepoImpl,
        public readonly customerOrders: CustomerOrderRepoImpl,
        public readonly employeeGrills: EmployeeGrillRepoImpl,
        public readonly employeeOrders: EmployeeOrderRepoImpl,
        public readonly employeeKitchenTerminals: EmployeeKitchenTerminalRepoImpl
    ) {
    }

    getNavigationService(): NavigationService {
        return this.navigationService;
    }
} 
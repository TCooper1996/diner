import { NavigationService } from '@core/services/NavigationService';
import { CustomerRepo } from '@core/repos/CustomerRepo';
import { OrderRepo } from '@core/repos/OrderRepo';
import { EmployeeRepo } from '@core/repos/EmployeeRepo';
import { SeatRepo } from '@core/repos/SeatRepo';
import { EntranceRepo } from '@core/repos/EntranceRepo';
import { GrillRepo } from '@core/repos/GrillRepo';
import { CustomerSeatRepo } from '@core/repos/CustomerSeatRepo';
import { CustomerOrderRepo } from '@core/repos/CustomerOrderRepo';
import { EmployeeGrillRepo } from '@core/repos/EmployeeGrillRepo';
import { EmployeeOrderRepo } from '@core/repos/EmployeeOrderRepo';
import { EmployeeKitchenTerminalRepo } from '../repos/EmployeeKitchenTerminalRepo';

/**
 * RestaurantState represents the current state of the restaurant.
 * It extends all repository interfaces to provide access to all restaurant entities.
 * 
 * Ideally, only actions should be able to modify the state of the restaurant.
 * RestaurantState should only contain real world objects and relationships, no agent messages.
 */
export interface RestaurantState {
    customers: CustomerRepo,
    orders: OrderRepo,
    employees: EmployeeRepo,
    seats: SeatRepo,
    entrances: EntranceRepo,
    grills: GrillRepo,
    customerSeats: CustomerSeatRepo,
    customerOrders: CustomerOrderRepo,
    employeeGrills: EmployeeGrillRepo,
    employeeOrders: EmployeeOrderRepo,
    employeeKitchenTerminals: EmployeeKitchenTerminalRepo,
    /**
     * Get the navigation service for the restaurant
     */
    getNavigationService(): NavigationService;
} 
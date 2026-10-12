import { CustomerOrderRepo } from '@core/repos/CustomerOrderRepo';

/**
 * Implementation of the CustomerOrderRepo interface that stores the relationships
 * between customers and orders using a single Map.
 */
export class CustomerOrderRepoImpl implements CustomerOrderRepo {
    private customerOrders: Map<string, string>; // customer_id -> order_id

    constructor() {
        this.customerOrders = new Map<string, string>();
    }

    getOrderOfCustomer(customerId: string): string {
        const orderId = this.customerOrders.get(customerId);
        if (!orderId) {
            throw new Error(`No order found for customer with ID ${customerId}`);
        }
        return orderId;
    }

    getCustomerOfOrder(orderId: string): string {
        for (const [customerId, assignedOrderId] of this.customerOrders.entries()) {
            if (assignedOrderId === orderId) {
                return customerId;
            }
        }
        throw new Error(`No customer found for order with ID ${orderId}`);
    }
} 
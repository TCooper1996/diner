import { Order } from '@core/entities/Order';

export interface OrderRepo {
    /**
     * Create a new order in the repository
     */
    createOrder(): Order;

    /**
     * Get an order by its ID
     */
    getOrder(orderId: string): Order;

    /**
     * Get all orders in the repository
     */
    getAllOrders(): Order[];

    /**
     * Update an existing order
     */
    updateOrder(order: Order): void;

    /**
     * Add a new order to the repository
     */
    addOrder(order: Order): void;
} 
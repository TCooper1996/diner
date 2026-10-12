import { Order, OrderStatus } from '@core/entities/Order';
import { OrderRepo } from '@core/repos/OrderRepo';

/**
 * Implementation of the OrderRepo interface that stores orders in a Map.
 */
export class OrderRepoImpl implements OrderRepo {
    private orders: Map<string, Order>;
    private nextOrderId: number;

    constructor() {
        this.orders = new Map<string, Order>();
        this.nextOrderId = 1;
    }

    createOrder(): Order {
        const orderId = `order_${this.nextOrderId}`;
        this.nextOrderId++;
        
        const order = new Order(
            orderId,
            OrderStatus.PENDING
        );
        
        this.orders.set(orderId, order);
        return order;
    }

    getOrder(orderId: string): Order {
        const order = this.orders.get(orderId);
        if (!order) {
            throw new Error(`No order found with ID ${orderId}`);
        }
        return order;
    }

    getAllOrders(): Order[] {
        return Array.from(this.orders.values());
    }

    updateOrder(order: Order): void {
        if (!this.orders.has(order.id)) {
            throw new Error(`No order found with ID ${order.id} to update`);
        }
        this.orders.set(order.id, order);
    }

    addOrder(order: Order): void {
        if (this.orders.has(order.id)) {
            throw new Error(`Order with ID ${order.id} already exists`);
        }
        this.orders.set(order.id, order);
    }
} 
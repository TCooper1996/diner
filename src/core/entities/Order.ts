/**
 * Represents the status of an order in the restaurant.
 */
export enum OrderStatus {
    PENDING = 'PENDING',
    COOKING = 'COOKING',
    READY = 'READY',
    DELIVERED = 'DELIVERED'
}

/**
 * Represents an order in the restaurant.
 */
export class Order {
    constructor(
        public readonly id: string,
        public status: OrderStatus
    ) {}

    /**
     * Check if the order is in a terminal state (DELIVERED).
     */
    isTerminal(): boolean {
        return this.status === OrderStatus.DELIVERED;
    }

    /**
     * Check if the order is ready to be delivered.
     */
    isReady(): boolean {
        return this.status === OrderStatus.READY;
    }

    /**
     * Check if the order is currently being cooked.
     */
    isCooking(): boolean {
        return this.status === OrderStatus.COOKING;
    }

    /**
     * Check if the order is pending.
     */
    isPending(): boolean {
        return this.status === OrderStatus.PENDING;
    }
} 
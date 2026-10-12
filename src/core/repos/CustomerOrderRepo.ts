export interface CustomerOrderRepo {
    /**
     * Get the order of a customer by their ID
     */
    getOrderOfCustomer(customerId: string): string;

    /**
     * Get the customer associated with a specific order ID
     */
    getCustomerOfOrder(orderId: string): string;
} 
export interface CustomerSeatRepo {
    /**
     * Get the seat number of a customer
     */
    getCustomerSeat(customerName: string): string | null;

    /**
     * Set the seat for a customer
     */
    setCustomerSeat(customerName: string, seatId: string): void;

    /**
     * Check if a seat is occupied
     */
    isSeatOccupied(seatId: string): boolean;
} 
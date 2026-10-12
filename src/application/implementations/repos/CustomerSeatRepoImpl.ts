import { CustomerSeatRepo } from '@core/repos/CustomerSeatRepo';

/**
 * Implementation of the CustomerSeatRepo interface that manages the relationship
 * between customers and seats using a Map.
 */
export class CustomerSeatRepoImpl implements CustomerSeatRepo {
    private customerSeats: Map<string, string>; // customer_name -> seat_id

    constructor() {
        this.customerSeats = new Map<string, string>();
    }

    getCustomerSeat(customerName: string): string | null {
        return this.customerSeats.get(customerName) || null;
    }

    setCustomerSeat(customerName: string, seatId: string): void {
        // Check if the seat is already occupied by another customer
        const existingCustomer = Object.entries(this.customerSeats)
            .find(([_, assignedSeatId]) => assignedSeatId === seatId)?.[0];
        if (existingCustomer && existingCustomer !== customerName) {
            throw new Error(`Seat ${seatId} is already occupied by ${existingCustomer}`);
        }
        this.customerSeats.set(customerName, seatId);
    }

    isSeatOccupied(seatId: string): boolean {
        return Object.values(this.customerSeats).includes(seatId);
    }

    getSeatOfCustomer(customerName: string): string | null {
        return this.customerSeats.get(customerName) || null;
    }

    getCustomerOfSeat(seatId: string): string | null {
        for (const [customerName, assignedSeatId] of this.customerSeats.entries()) {
            if (assignedSeatId === seatId) {
                return customerName;
            }
        }
        return null;
    }
} 
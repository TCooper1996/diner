import { Seat } from '@core/entities/Seat';

export interface SeatRepo {
    /**
     * Get a specific seat by its ID
     */
    getSeat(seatId: string): Seat;

    /**
     * Get all seats in the restaurant
     */
    getAllSeats(): Seat[];
} 
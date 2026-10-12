import { Seat } from '@core/entities/Seat';
import { SeatRepo } from '@core/repos/SeatRepo';

/**
 * Implementation of the SeatRepo interface that stores seats in a Map.
 */
export class SeatRepoImpl implements SeatRepo {
    private seats: Map<string, Seat>;

    constructor() {
        this.seats = new Map<string, Seat>();
    }

    getSeat(seatId: string): Seat {
        const seat = this.seats.get(seatId);
        if (!seat) {
            throw new Error(`No seat found with ID ${seatId}`);
        }
        return seat;
    }

    getAllSeats(): Seat[] {
        return Array.from(this.seats.values());
    }

    addSeat(seat: Seat): void {
        if (this.seats.has(seat.seatId)) {
            throw new Error(`Seat with ID ${seat.seatId} already exists`);
        }
        this.seats.set(seat.seatId, seat);
    }
} 
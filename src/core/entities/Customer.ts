import { Position } from '../common/Position';

/**
 * Represents the status of a customer in the restaurant.
 */
export enum CustomerStatus {
    WAITING = 'WAITING',
    SEATED = 'SEATED',
    ORDERING = 'ORDERING',
    EATING = 'EATING',
    LEAVING = 'LEAVING'
}

const customerNames = [
    "Charlie", "Diana", "Eve", "Frank", "Grace", "Heidi",
    "Ivan", "Judy", "Karl", "Leo", "Mallory", "Nina", "Oscar", "Peggy",
    "Quentin", "Rupert", "Sybil", "Trent", "Uma", "Victor", "Walter"
];

const customerLastnames = [
    "Smith", "Johnson", "Williams", "Jones", "Brown", "Davis", "Miller",
    "Wilson", "Moore", "Taylor", "Anderson", "Thomas", "Jackson", "White",
    "Harris", "Martin", "Thompson", "Garcia", "Martinez", "Robinson"
];

const names = customerNames.map((f, i) => `${f} ${customerLastnames[i]}`);
let nameIndex = 0;

function nextName(): string {
    const name = names[nameIndex];
    nameIndex = (nameIndex + 1) % names.length;
    return name;
}

/**
 * Represents a customer in the restaurant.
 */
export class Customer {
    private _position: { x: number; y: number };
    private _targetPosition: { x: number; y: number } | null;
    private _hasOrder: boolean;
    private _isSeated: boolean;
    private _status: CustomerStatus;
    private _waitingTime: number;
    private _patience: number;
    private _eatingTime: number;

    constructor(
        public readonly id: string,
        position: { x: number; y: number },
        waitingTime: number = 0,
        patience: number = 50,
        status: CustomerStatus = CustomerStatus.WAITING,
        eatingTime: number = 0
    ) {
        this._position = position;
        this._targetPosition = null;
        this._hasOrder = false;
        this._isSeated = false;
        this._status = status;
        this._waitingTime = waitingTime;
        this._patience = patience;
        this._eatingTime = eatingTime;
    }

    /**
     * Get the current position of the customer.
     */
    get position(): { x: number; y: number } {
        return this._position;
    }

    /**
     * Set the current position of the customer.
     */
    set position(pos: { x: number; y: number }) {
        this._position = pos;
    }

    /**
     * Get the target position of the customer.
     */
    get targetPosition(): { x: number; y: number } | null {
        return this._targetPosition;
    }

    /**
     * Set the target position of the customer.
     */
    set targetPosition(pos: { x: number; y: number } | null) {
        this._targetPosition = pos;
    }

    /**
     * Check if the customer has an order.
     */
    get hasOrder(): boolean {
        return this._hasOrder;
    }

    /**
     * Set whether the customer has an order.
     */
    set hasOrder(hasOrder: boolean) {
        this._hasOrder = hasOrder;
    }

    /**
     * Check if the customer is seated.
     */
    get isSeated(): boolean {
        return this._isSeated;
    }

    /**
     * Set whether the customer is seated.
     */
    set isSeated(isSeated: boolean) {
        this._isSeated = isSeated;
    }

    /**
     * Get the current status of the customer.
     */
    get status(): CustomerStatus {
        return this._status;
    }

    /**
     * Set the current status of the customer.
     */
    set status(status: CustomerStatus) {
        this._status = status;
    }

    /**
     * Get the waiting time of the customer.
     */
    get waitingTime(): number {
        return this._waitingTime;
    }

    /**
     * Set the waiting time of the customer.
     */
    set waitingTime(time: number) {
        this._waitingTime = time;
    }

    /**
     * Get the patience of the customer.
     */
    get patience(): number {
        return this._patience;
    }

    /**
     * Set the patience of the customer.
     */
    set patience(patience: number) {
        this._patience = patience;
    }

    /**
     * Get the eating time of the customer.
     */
    get eatingTime(): number {
        return this._eatingTime;
    }

    /**
     * Set the eating time of the customer.
     */
    set eatingTime(time: number) {
        this._eatingTime = time;
    }

    /**
     * Check if the customer has reached their target position.
     */
    hasReachedTarget(): boolean {
        if (!this._targetPosition) {
            return true;
        }
        return this._position.x === this._targetPosition.x && 
               this._position.y === this._targetPosition.y;
    }

    /**
     * Move the customer towards their target position.
     */
    moveTowardsTarget(): void {
        if (!this._targetPosition) {
            return;
        }

        const dx = this._targetPosition.x - this._position.x;
        const dy = this._targetPosition.y - this._position.y;

        if (Math.abs(dx) > Math.abs(dy)) {
            this._position.x += Math.sign(dx);
        } else {
            this._position.y += Math.sign(dy);
        }
    }

    /**
     * Convert the customer to a prompt string.
     */
    toPrompt(): string {
        return `
Customer: ${this.id}
    Location: (${this._position.x}, ${this._position.y})
    Status: ${this._status}
    Waiting Time: ${this._waitingTime}
    Patience: ${this._patience}
    Eating Time: ${this._eatingTime}
    Has Order: ${this._hasOrder}
    Is Seated: ${this._isSeated}
`;
    }

    startEating(): void {
        this.status = CustomerStatus.EATING;
    }

    isDone(): boolean {
        return this.status === CustomerStatus.EATING && this.eatingTime >= 3;
    }
} 
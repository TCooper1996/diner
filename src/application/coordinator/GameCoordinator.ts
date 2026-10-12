import { EventEmitter } from 'events';
import { GameSession } from '@core/models/GameSession';
import { GameLoop } from '../game/GameLoop';
import { RestaurantState } from '@/core/models/RestaurantState';

/**
 * GameCoordinator manages the game loop and handles events.
 * It acts as the main coordinator between the game loop and the UI.
 * 
 * This is an application service that coordinates between the game loop
 * and the UI layer, handling events and state updates.
 */
export class GameCoordinator {
    private gameLoop: GameLoop;
    private eventEmitter: EventEmitter;
    private currentGameTask: Promise<void> | null = null;
    private isPaused: boolean = false;

    constructor(
        initialWorld: RestaurantState,
        initialSession: GameSession,
        eventEmitter: EventEmitter
    ) {
        this.eventEmitter = eventEmitter;
        this.gameLoop = new GameLoop(initialWorld, initialSession);
    }

    /**
     * Start the game coordinator
     */
    async start(): Promise<void> {
        // Start event handling
        this.setupEventHandlers();
        
        // Start game loop
        await this.runGameLoop();
    }

    /**
     * Set up event handlers for game events
     */
    private setupEventHandlers(): void {
        this.eventEmitter.on('PAUSE', () => {
            this.isPaused = true;
        });

        this.eventEmitter.on('RESUME', () => {
            this.isPaused = false;
        });

        this.eventEmitter.on('RESET', async () => {
            if (this.currentGameTask) {
                // Cancel current game loop
                this.currentGameTask = null;
            }
            // Start new game loop
            await this.runGameLoop();
        });
    }

    /**
     * Run the game loop and emit state updates
     */
    private async runGameLoop(): Promise<void> {
        this.currentGameTask = (async () => {
            for await (const state of this.gameLoop.run()) {
                // Skip state updates if paused
                if (this.isPaused) {
                    await new Promise(resolve => setTimeout(resolve, 100));
                    continue;
                }
                this.eventEmitter.emit('STATE_UPDATE', state);
            }
        })();
    }
} 
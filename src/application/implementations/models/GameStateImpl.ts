import { GameState } from '@core/models/GameState';
import { ActiveTurn } from '@core/models/ActiveTurn';
import { NavigationService } from '@core/services/NavigationService';
import { AgentService } from '@core/services/AgentService';
import { ActionRepo } from '@core/repos/ActionRepo';
import { GameLogRepo } from '@core/repos/GameLogRepo';
import { RestaurantState } from '@core/models/RestaurantState';
import { ActionRepoImpl } from '../repos/ActionRepoImpl';
import { GameLogRepoImpl } from '../repos/GameLogRepoImpl';
import { RestaurantStateImpl } from './RestaurantStateImpl';

/**
 * GameStateImpl implements the GameState interface using composition.
 * It combines game-specific functionality with restaurant state.
 */
export class GameStateImpl implements GameState {
    private tick: number = 0;
    private activeTurn: ActiveTurn;
    public readonly actions: ActionRepo;
    public readonly logs: GameLogRepo;
    public readonly agentService: AgentService;
    public readonly worldState: RestaurantState;

    constructor(
        navigationService: NavigationService,
        agentService: AgentService,
        activeTurn: ActiveTurn
    ) {
        this.activeTurn = activeTurn;
        this.agentService = agentService;
        
        // Initialize repositories
        this.actions = new ActionRepoImpl();
        this.logs = new GameLogRepoImpl();
        this.worldState = new RestaurantStateImpl(navigationService);
    }

    getTick(): number {
        return this.tick;
    }

    getWhoseTurn(): ActiveTurn {
        return this.activeTurn;
    }

    setWhoseTurn(turn: ActiveTurn): void {
        this.activeTurn = turn;
    }

    copy(): GameState {
        // Create a new instance with the same services
        const newState = new GameStateImpl(
            this.worldState.getNavigationService(),
            this.agentService,
            this.activeTurn
        );

        // Copy the game state properties
        newState.tick = this.tick;

        // Copy repository data
        // Note: Each repository implementation should handle its own copying
        // This is a simplified version - you'll need to implement proper copying
        // for each repository's data

        return newState;
    }
} 
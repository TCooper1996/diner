import { GameTurn } from "../models/TurnTypes";

export interface TurnRepository {

    addTurn(turn: GameTurn): void
}
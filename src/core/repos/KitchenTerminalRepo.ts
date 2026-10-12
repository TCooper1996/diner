import { KitchenTerminal } from "../entities/KitchenTerminal";

export interface KitchenTerminalRepo {
  getKitchenTerminal(id: string): KitchenTerminal;
  addKitchenTerminal(kitchenTerminal: KitchenTerminal): void;
}


import { Action } from "./Action";

export type GameTurn = {turn: number} & ({type: "customer_turn", turn: CustomerTurn} | {type: "employee_turn", turn: EmployeeTurn})

export type EmployeeTurn = {
    employeeId: string;
    action: Action;
    action_selection_info: ActionSelectionInfo;
}

export type ActionSelectionInfo = {
    type: "agent_selection", 
    info: AgentSelection
} | {type: "continued", effect: string}

export type AgentSelection = {
    agent_response: string
    verification_error: string | null
}

export type CustomerTurn = {
    
}



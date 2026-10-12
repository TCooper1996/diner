import { AgentService } from '@core/services/AgentService';
import { ActionSelection } from '@core/models/ActionSelection';
import { GameLogRepo } from '@core/repos/GameLogRepo';
import { Action } from '@core/models/Action';
import { LLM } from '@agents/employeeAgent';
import { Claude } from '@agents/models/Claude';
import { StandardMessage, ResponseMessage, ToolInvocationMessage, ToolResultMessage, HumanMessage, SystemMessage } from '@agents/models/Model';
import { parseTool } from '@actions/parseTool';

/**
 * Implementation of the AgentService interface that uses an LLM to choose actions.
 */
export class AgentServiceImpl implements AgentService {
    private agentCache: Map<string, LLM>;
    private instructions: Map<string, string>;
    private allowedActions: Map<string, typeof Action[]>;

    constructor(
        instructions: Record<string, string>,
        allowedActions: Record<string, typeof Action[]>,
        private readonly gameLogRepo: GameLogRepo
    ) {
        this.instructions = new Map(Object.entries(instructions));
        this.allowedActions = new Map(Object.entries(allowedActions));
        this.agentCache = new Map();

        // Initialize agents for each employee
        for (const [employeeName, _] of this.instructions) {
            const actions = this.allowedActions.get(employeeName) || [];
            this.agentCache.set(employeeName, new LLM(new Claude(actions)));
        }
    }

    async chooseAction(employeeName: string, stateMessage: string): Promise<ActionSelection> {
        const messages = this.getMessageHistory(employeeName);
        const agent = this.agentCache.get(employeeName);
        if (!agent) {
            throw new Error(`No agent found for employee ${employeeName}`);
        }

        const response = await agent.invokeCached(
            this.instructions.get(employeeName) || '',
            stateMessage,
            messages
        );

        const action = parseTool(response.toolName, response.toolArgs);
        return {
            action,
            description: response.originalResponse.content
        };
    }

    private getMessageHistory(employeeName: string): StandardMessage[] {
        const agent = this.agentCache.get(employeeName);
        if (!agent) {
            throw new Error(`No agent found for employee ${employeeName}`);
        }

        // Get all logs related to the employee
        const logs = this.gameLogRepo.getGameLogs();
        const employeeLogs = logs.filter(log => log.getEmployeeId() === employeeName);
        const messages: StandardMessage[] = [];
        let toolIdCounter = 0;

        for (const log of employeeLogs) {
            if (log.isContinuedAction()) {
                messages.push(new HumanMessage(log.getExecutionResults()));
            } else {
                for (const actionLog of log.getActionSelectionLogs()) {
                    messages.push(new ResponseMessage(actionLog.agentResponse()));
                    const action = actionLog.getAction();
                    const actionName = action.constructor.name;
                    const actionArgs = Object.fromEntries(
                        Object.entries(action).filter(([key]) => !key.startsWith('_'))
                    );

                    messages.push(new ToolInvocationMessage(
                        actionName,
                        actionArgs,
                        toolIdCounter.toString()
                    ));

                    messages.push(new ToolResultMessage(
                        actionName,
                        actionLog.getVerificationError() || "Successful",
                        toolIdCounter.toString(),
                        actionLog.getVerificationError() !== null
                    ));

                    toolIdCounter++;
                }
            }
        }

        return messages;
    }
} 
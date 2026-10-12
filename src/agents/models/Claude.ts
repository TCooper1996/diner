import { Model, StandardMessage, ResponseMessage, ToolInvocationMessage } from './Model';
import { Action } from '@core/models/Action';

/**
 * Implementation of the Model interface using Claude.
 */
export class Claude implements Model {
    constructor(private readonly allowedActions: typeof Action[]) {}

    async ainvoke(messages: StandardMessage[]): Promise<[ResponseMessage, ToolInvocationMessage | null]> {
        // TODO: Implement actual Claude API call
        // For now, return a mock response
        const response = new ResponseMessage("I will help with that.");
        const toolCall = new ToolInvocationMessage(
            "WaitAction",
            {},
            "0"
        );
        return [response, toolCall];
    }
} 
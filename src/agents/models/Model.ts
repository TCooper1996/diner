/**
 * Base interface for all message types in the agent system.
 */
export interface BaseMessage {
    content: string;
}

/**
 * Response message from the agent.
 */
export class ResponseMessage implements BaseMessage {
    constructor(public content: string) {}
}

/**
 * Tool invocation message from the agent.
 */
export class ToolInvocationMessage implements BaseMessage {
    constructor(
        public tool: string,
        public toolInput: Record<string, any>,
        public toolId: string
    ) {}
    get content(): string {
        return `Tool: ${this.tool}, Input: ${JSON.stringify(this.toolInput)}`;
    }
}

/**
 * Tool result message from the agent.
 */
export class ToolResultMessage implements BaseMessage {
    constructor(
        public tool: string,
        public toolOutput: string,
        public toolId: string,
        public isError: boolean
    ) {}
    get content(): string {
        return `Tool: ${this.tool}, Output: ${this.toolOutput}, Error: ${this.isError}`;
    }
}

/**
 * Human message to the agent.
 */
export class HumanMessage implements BaseMessage {
    constructor(public content: string) {}
}

/**
 * System message to the agent.
 */
export class SystemMessage implements BaseMessage {
    constructor(public content: string) {}
}

/**
 * Union type of all possible message types.
 */
export type StandardMessage = 
    | ResponseMessage 
    | ToolInvocationMessage 
    | ToolResultMessage 
    | HumanMessage 
    | SystemMessage;

/**
 * Interface for LLM models.
 */
export interface Model {
    /**
     * Invoke the model with a list of messages.
     * Returns a tuple of [response message, optional tool invocation].
     */
    ainvoke(messages: StandardMessage[]): Promise<[ResponseMessage, ToolInvocationMessage | null]>;
} 
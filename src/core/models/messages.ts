export interface StandardMessage {
    content: string;
    role: string;
}

export interface ResponseMessage extends StandardMessage {
    role: 'assistant';
}

export interface ToolInvocationMessage extends StandardMessage {
    role: 'tool';
    tool: string;
    toolId: string;
    toolInput: any;
}

export interface ToolResultMessage extends StandardMessage {
    role: 'tool';
    tool: string;
    toolId: string;
    toolOutput: string;
    isError: boolean;
} 
import { Model, StandardMessage, ResponseMessage, ToolInvocationMessage } from './models/Model';

/**
 * Result of an LLM invocation.
 */
export interface LLMResult {
    toolName: string;
    toolArgs: Record<string, any>;
    toolId: string;
    prompt: string;
    originalResponse: ResponseMessage;
    gameStatePrompt: string;
    messages: string[];
}

/**
 * LLM wrapper for employee agents.
 */
export class LLM {
    private cache: Map<string, LLMResult> = new Map();

    constructor(private readonly model: Model) {}

    async invokeCached(prompt: string, stateMessage: string, messages: StandardMessage[]): Promise<LLMResult> {
        const key = JSON.stringify({
            prompt,
            stateMessage,
            messages: messages.map(m => m.content)
        });

        if (this.cache.has(key)) {
            return this.cache.get(key)!;
        }

        const response = await this.invoke(prompt, stateMessage, messages);
        this.cache.set(key, response);
        return response;
    }

    private async invoke(prompt: string, stateMessage: string, messages: StandardMessage[]): Promise<LLMResult> {
        const systemMessage = new SystemMessage(`Instructions: ${prompt}`);
        const humanMessage = new HumanMessage(stateMessage);

        let i = 0;
        while (true) {
            const [text, toolCall] = await this.model.ainvoke([
                systemMessage,
                ...messages,
                humanMessage
            ]);

            if (!toolCall) {
                if (i > 3) {
                    throw new Error("Failed to get a valid response from the LLM");
                }
                messages.push(text);
                messages.push(new HumanMessage("Error: You must invoke exactly one tool. Try again."));
                i++;
                continue;
            }

            return {
                toolName: toolCall.tool,
                toolArgs: toolCall.toolInput,
                toolId: toolCall.toolId,
                prompt,
                originalResponse: text,
                gameStatePrompt: stateMessage,
                messages: messages.map(m => m.content)
            };
        }
    }
} 
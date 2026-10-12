export interface ActionResult {
    message: string;
    repeat: boolean;
}

export type ActionValidationResult = {
    success: true;
} | {
    success: false;
    error_message: string;
}
import { RestaurantState } from '../core/models/RestaurantState';
import { ActionResult, ValidationResult } from '../core/models/Action';
import { ActionDefinition, ActionHandler } from './types';

export const waitAction: ActionDefinition = {
  name: 'wait',
  description: 'Tool for waiting (taking no action)',
  parameters: {
    type: 'object',
    properties: {},
    required: []
  }
};

export const waitHandler: ActionHandler = {
  validate: (state: RestaurantState, employeeId: string): ValidationResult => {
    return { success: true };
  },

  execute: (state: RestaurantState, employeeId: string): ActionResult => {
    return {
      message: `${employeeId} is waiting for the next instruction.`,
      repeat: false
    };
  }
}; 
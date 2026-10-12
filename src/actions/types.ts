import { ActionResult, ValidationResult } from '../core/models/Action';
import { RestaurantState } from '../core/models/RestaurantState';
import { NavigationService } from '../core/services/NavigationService';
import { Employee } from '../core/entities/Employee';
import { Customer } from '../core/entities/Customer';
import { Order } from '../core/entities/Order';
import { Seat } from '../core/entities/Seat';
import { Grill } from '../core/entities/Grill';
import { CustomerStatus } from '../core/entities/Customer';
import { OrderStatus } from '../core/entities/Order';

export interface ActionDefinition {
  name: string;
  description: string;
  parameters: {
    type: 'object';
    properties: Record<string, {
      type: string;
      description: string;
    }>;
    required: string[];
  };
}

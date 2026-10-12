import { Customer } from '@core/entities/Customer';

export interface CustomerRepo {
    getAllCustomers(): Customer[];
    getCustomer(customerId: string): Customer;
    getCount(): number;
    addCustomer(customer: Customer): void;
    updateCustomer(customer: Customer): void;
} 